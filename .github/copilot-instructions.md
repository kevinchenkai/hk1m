# hk1m AI Stock Trading Agent - Developer Guide

## 项目概述
这是一个AI驱动的港股量化交易系统，目标在一年内实现1M港币初始资金的20%收益率。系统基于Futu API获取市场数据，使用LLM（DeepSeek/Gemini）生成交易策略，当前聚焦于HK.00700（腾讯控股）和HK.09988（阿里巴巴-W）两只股票。

**初始状态**: 现金 1,000,000港币 | HK.00700: 1000股(成本620) | HK.09988: 2000股(成本155)  
**托管起始日期**: 2025-10-01 (定义在 `src/build_prompt.py` 的 `START_DAY`)

## 核心架构

### 数据流水线
```
Futu API → K线/订单数据 → JSON Lines 存储 → Prompt构建 → LLM预测 → 交易决策
```

### 关键组件
1. **数据获取层** (`src/get_*.py`): 通过本地Futu OpenD服务(127.0.0.1:11111)获取实时数据
2. **Prompt生成** (`src/build_prompt.py`): 组合历史数据与策略模板生成LLM输入
3. **LLM调用** (`src/call_gemini.py`, `src/price_predict.py`): 支持Gemini和DeepSeek模型
4. **持仓计算** (`src/calc_holdings.py`): 根据订单历史计算当前资金和持仓状态

### 目录结构约定
```
datasets/
  klines/HK/{YYYYMM}/HK.{CODE}_{YYMMDD}.jsonl    # 每日K线快照
  klines/HK/HK.{CODE}_lastest.jsonl              # 最新K线数据（用于prompt）
  orders/HK/{YYYYMM}/HK.{CODE}_order.jsonl       # 订单历史
  ground/HK.{CODE}_gt.jsonl                      # 预测vs实际对比数据
prompts/combined_prompt.txt                      # 生成的完整prompt
strategy/stg{NN}.template                        # 策略模板（支持变量替换）
```

## 开发工作流

### 日常运行脚本
使用 `run.sh` 编排完整流程（获取数据→构建prompt→调用LLM），脚本包含严格错误处理和日志记录。

### Futu API依赖
**必须启动本地OpenD服务**: 所有API调用通过 `common.py` 的 `create_quote_context()` 和 `create_trade_context()` 连接到本地服务，默认端口11111。

### 添加新股票
1. 在 `src/common.py` 的 `STOCK_CODES` 列表添加代码
2. 对应调整 `src/build_prompt.py` 中的数据读取和拼接逻辑
3. 更新 `strategy/*.template` 模板的股票引用

### 策略模板系统
模板使用占位符进行变量替换（见 [strategy/stg03.template](strategy/stg03.template)）:
- `{START_DAY}`, `{TODAY}`, `{DAY}` - 时间维度
- `{PORTFOLIO}` - 由 `calc_holdings.py` 计算的当前状态
- `{KLINE_DATA}`, `{ORDER_DATA}`, `{GT_DATA}` - 历史数据

## 项目特定约定

### JSONL数据格式
所有市场数据以JSON Lines格式存储，关键字段:
- **K线**: code, name, time_key, open, close, high, low, volume, turnover, pe_ratio, turnover_rate, last_close
- **订单**: create_time, code, trd_side (BUY/SELL), price, qty, order_status (FILLED_ALL/CANCELLED_ALL)
- **Ground Truth**: `| 日期 | 股票代码 | 实际高 | 实际低 | DeepSeek预测高 | DeepSeek预测低 | Gemini预测高 | Gemini预测低 |`

### 文件命名模式
- K线文件: `HK.{CODE}_{YYMMDD}.jsonl` (例: `HK.00700_251216.jsonl`)
- 订单文件: `HK.{CODE}_order.jsonl`
- Latest文件: `HK.{CODE}_lastest.jsonl` (始终指向最新数据)

### 日期处理
项目混用两种日期格式，需注意转换:
- 文件名: `YYMMDD` (例: 251216)
- 数据内容: `YYYY-MM-DD` (例: 2025-12-16)
- GT数据: `YYYYMMDD` (例: 20251216)

## LLM集成

### API密钥管理
- Gemini: 硬编码在 `call_gemini.py` (TODO: 迁移至环境变量)
- DeepSeek/Kimi: 通过 `.env` 文件的 `KSC_API_KEY` 配置

### 模型切换
在 `src/price_predict.py` 顶部切换 `MODEL` 变量:
```python
MODEL = "deepseek-v3.2-exp"  # 或 "kimi-k2-thinking"
```

### Prompt构建流程
[build_prompt.py](src/build_prompt.py) → 读取策略模板 → 替换变量 → 输出 `prompts/combined_prompt.txt`

## 常见任务

### 获取最近N天K线数据
```bash
python src/get_klines.py  # 默认10天，见 get_all_stocks_kline(days=10)
```

### 重新计算持仓
[calc_holdings.py](src/calc_holdings.py) 从初始状态开始，按时间顺序处理所有FILLED_ALL订单，输出当前现金和持仓明细。

### 调试数据流
1. 检查 `datasets/klines/HK/HK.{CODE}_lastest.jsonl` 确认最新数据
2. 运行 `python src/build_prompt.py` 生成prompt
3. 查看 `prompts/combined_prompt.txt` 验证数据完整性
4. 手动调用LLM或运行 `src/call_gemini.py`/`src/price_predict.py`

## 测试与验证

### 数据完整性检查
- 确保JSONL文件每行都是合法JSON（使用 `jq` 验证）
- 订单数据必须包含 `order_status` 字段用于过滤

### 预测评估
[ground truth文件](datasets/ground/HK.00700_gt.jsonl) 记录每日预测vs实际，用于回测策略有效性。

## 注意事项

1. **API速率限制**: `get_klines.py` 使用 `delay=1` 避免频繁请求，修改时保留此机制
2. **交易市场**: 交易上下文锁定为港股市场 (`TrdMarket.HK`) 和富途证券 (`SecurityFirm.FUTUSECURITIES`)
3. **持仓计算**: 永远从 `calc_holdings.py` 获取最新状态，勿手动估算
4. **策略更新**: 修改策略模板后需重新运行 `build_prompt.py` 生成新prompt

## 参考资源
- [Futu API文档](https://openapi.futunn.com/futu-api-doc/)
- [策略模板](strategy/stg03.template) - 当前使用的prompt结构
- [通用工具函数](src/common.py) - 所有路径生成和数据操作
