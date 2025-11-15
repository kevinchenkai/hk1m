# 实时K线：https://openapi.futunn.com/futu-api-doc/quote/get-kl.html
# 历史K线：https://openapi.futunn.com/futu-api-doc/quote/request-history-kline.html

from futu import *
import time
from common import *

def get_stock_kline(stock_code, days=10, kl_type=KLType.K_DAY, au_type=AuType.QFQ):
    """
    获取单只股票的K线数据
    
    Args:
        stock_code (str): 股票代码
        days (int): 获取天数，默认10天
        kl_type: K线类型，默认日K
        au_type: 复权类型，默认前复权
    
    Returns:
        tuple: (成功标志, 数据或错误信息)
    """
    quote_ctx = create_quote_context()
    
    try:
        # 订阅K线数据
        ret_sub, err_message = quote_ctx.subscribe([stock_code], [SubType.K_DAY], 
                                                  subscribe_push=False, session=Session.ALL)
        
        if ret_sub == RET_OK:
            # 获取K线数据
            ret, data = quote_ctx.get_cur_kline(stock_code, days, kl_type, au_type)
            if ret == RET_OK:
                return True, data
            else:
                return False, f"获取K线数据失败: {data}"
        else:
            return False, f"订阅失败: {err_message}"
            
    except Exception as e:
        return False, f"请求异常: {str(e)}"
    finally:
        quote_ctx.close()

def save_kline_data(stock_code, data):
    """
    保存K线数据到文件
    
    Args:
        stock_code (str): 股票代码
        data: K线数据 DataFrame
    """
    filepath = get_kline_filepath(stock_code)
    save_data_to_jsonl(data, filepath)
    print_success(stock_code, filepath, "K线数据")

def get_all_stocks_kline(stock_codes=None, days=10, delay=1):
    """
    获取所有股票的K线数据
    
    Args:
        stock_codes (list): 股票代码列表，默认使用STOCK_CODES
        days (int): 获取天数
        delay (int): 请求间隔时间（秒），避免频繁请求
    """
    if stock_codes is None:
        stock_codes = STOCK_CODES
        
    print(f"开始获取 {len(stock_codes)} 只股票的K线数据...")
    print("=" * 50)
    
    success_count = 0
    failed_stocks = []
    
    for i, stock_code in enumerate(stock_codes, 1):
        print(f"[{i}/{len(stock_codes)}] 正在处理: {stock_code}")
        
        # 获取K线数据
        success, result = get_stock_kline(stock_code, days)
        
        if success:
            # 保存数据
            save_kline_data(stock_code, result)
            success_count += 1
        else:
            print_error(stock_code, result, "K线数据")
            failed_stocks.append((stock_code, result))
        
        # 添加延迟，避免请求过于频繁
        if i < len(stock_codes):
            time.sleep(delay)
    
    # 输出统计结果
    print("=" * 50)
    print(f"处理完成！成功: {success_count}/{len(stock_codes)}")
    
    if failed_stocks:
        print(f"失败的股票 ({len(failed_stocks)}):")
        for stock_code, error in failed_stocks:
            print(f"  - {stock_code}: {error}")

if __name__ == "__main__":
    # 获取所有股票的K线数据
    get_all_stocks_kline(days=64, delay=1)
