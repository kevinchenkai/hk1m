from futu import *
import pandas as pd
from common import *

def load_order_data(stock_code):
    """
    加载订单数据
    
    Args:
        stock_code (str): 股票代码
    
    Returns:
        str or pd.DataFrame: 订单数据
    """
    filepath = get_order_filepath(stock_code)
    print(f"加载订单数据文件: {filepath}")
    
    try:
        return read_file(filepath)
    except FileNotFoundError:
        print(f"订单数据文件不存在: {filepath}")
        return pd.DataFrame()

def save_order_data(stock_code, data):
    """
    保存订单数据
    
    Args:
        stock_code (str): 股票代码
        data (pd.DataFrame): 订单数据
    """
    filepath = get_order_filepath(stock_code)
    
    # 指定要保留的列和日期列
    columns_to_keep = ['create_time', 'code', 'trd_side', 'price', 'qty', 'order_status']
    date_columns = ['create_time']
    
    save_data_to_jsonl(data, filepath, columns_to_keep, date_columns)
    print_success(stock_code, filepath, "订单数据")

def get_order_data(stock_code, p_day=10):
    """
    获取订单数据
    
    Args:
        stock_code (str): 股票代码
        p_day (int): 获取天数，默认10天
    """
    trd_ctx = create_trade_context()
    
    try:
        p_start, p_end = format_date_range(p_day)
        ret, data = trd_ctx.history_order_list_query(code=stock_code, start=p_start, end=p_end)
        
        if ret == RET_OK:
            save_order_data(stock_code, data)
        else:
            print_error(stock_code, data, "订单数据")
    finally:
        trd_ctx.close()

def main():
    stock_code = 'HK.00700'
    get_order_data(stock_code, p_day=60)
    
    stock_code = 'HK.09988'
    get_order_data(stock_code, p_day=60)

if __name__ == '__main__':
    main()