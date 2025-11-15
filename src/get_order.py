from futu import *
from datetime import datetime, timedelta
import pandas as pd

def load_order_data(stock_code, data_dir='./data'):
    sub_dir = stock_code.split('.')[0]
    month = datetime.now().strftime('%Y%m')
    full_dir = os.path.join(data_dir, sub_dir, month)
    filename = f"{stock_code}_order.jsonl"
    filepath = os.path.join(full_dir, filename)
    print(f"加载订单数据文件: {filepath}")
    
    if os.path.exists(filepath):
        #data = pd.read_json(filepath, orient='records', lines=True)
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
        return data
    else:
        print(f"订单数据文件不存在: {filepath}")
        return pd.DataFrame()

def save_order_data(stock_code, data, data_dir='./data'):
    # 确保数据目录存在
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 子目录：HK
    sub_dir = stock_code.split('.')[0]
    month = datetime.now().strftime('%Y%m')
    full_dir = os.path.join(data_dir, sub_dir, month)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)

    # 生成文件名：股票代码_日期.jsonl
    filename = f"{stock_code}_order.jsonl"
    filepath = os.path.join(full_dir, filename)
    
    # 保存数据
    columns_to_keep = ['create_time', 'code', 'trd_side', 'price', 'qty', 'order_status']
    data = data[columns_to_keep]
    # 处理create_time字段
    data['create_time'] = pd.to_datetime(data['create_time']).dt.strftime('%Y-%m-%d')

    data.to_json(filepath, orient='records', lines=True, force_ascii=False)
    print(f"✓ {stock_code} 订单数据已保存到: {filepath}")

def get_order_data(stock_code, p_day=10):
    trd_ctx = OpenSecTradeContext(filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, security_firm=SecurityFirm.FUTUSECURITIES)
    p_end = datetime.now().strftime('%Y-%m-%d')
    p_start = (datetime.now() - timedelta(days=p_day)).strftime('%Y-%m-%d')
    ret, data = trd_ctx.history_order_list_query(code=stock_code, start=p_start, end=p_end)
    if ret == RET_OK:
        #print(data)
        save_order_data(stock_code, data)
    else:
        print('history_order_list_query error: ', data)
    trd_ctx.close()

def main():
    stock_code = 'HK.00700'
    get_order_data(stock_code, p_day=60)
    
    stock_code = 'HK.09988'
    get_order_data(stock_code, p_day=60)
    #data = load_order_data(stock_code)
    #print(data)

if __name__ == '__main__':
    main()
