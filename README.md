# hk1m

> 1 Year, 1M HK, Stock Agent.  
> **目标：2026年，200万港币，AI Agent 投资策略，目标年收益20%**

## 📁 项目结构

```
hk1m/
├── datasets/          # 必要的数据
│   ├── ground/
│   ├── klines/
│   ├── orders/
│   └── prompts/
├── logs/              # 日志文件
├── src/               # 源代码
│   ├── get_klines.py  # 获取K线数据
│   ├── get_order.py # 获取下单数据
│   └── build_prompt.py # 生成大模型执行 prompt 
└── README.md
```

## 🔧 功能模块

| 目录 | 描述 |
|------|------|
| `./datasets` | 必要的数据存储 |
| `./prompts` | 交易指令模板 |
| `./src` | 核心源代码 |

## 📊 Futu API 接口

### 账户管理
- [查询账号资金](https://openapi.futunn.com/futu-api-doc/trade/get-funds.html)
- [查询持仓](https://openapi.futunn.com/futu-api-doc/trade/get-position-list.html)

### 行情数据
- [获取实时K线](https://openapi.futunn.com/futu-api-doc/quote/get-kl.html)
- [获取实时报价](https://openapi.futunn.com/futu-api-doc/quote/get-stock-quote.html)

### 交易记录
- [查询历史订单](https://openapi.futunn.com/futu-api-doc/trade/get-history-order-list.html)
- [查询历史成交](https://openapi.futunn.com/futu-api-doc/trade/get-history-order-fill-list.html)

### 交易操作
- [自动下单](https://openapi.futunn.com/futu-api-doc/trade/place-order.html)

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/kevinchenkai/hk1m.git
cd hk1m

# 安装依赖
pip install -r requirements.txt

# 运行示例
python src/get_klines.py  #获取近期K线数据
python src/get_order.py  #获取下单历史数据
python src/build_prompt.py  #生成给大模型执行 Prompt
```

## 📈 投资策略

AI Agent 将通过以下步骤实现自动投资：

1. **数据收集**：获取实时K线和报价数据
2. **策略分析**：基于历史数据和AI模型进行价格预测
3. **风险控制**：设置止损止盈策略
4. **自动交易**：根据策略自动执行买卖操作

---

*最后更新：2025年11月15日*

