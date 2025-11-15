import os
from common import *

def build_stock_prompt(stock_code, stg='stg03'):
    """
    构建股票提示语
    
    Args:
        stock_code (str): 股票代码
        stg (int): 阶段，默认1
    """
    try:
        # 读取K线数据
        kline_filepath = get_kline_filepath(stock_code)
        kline_content = read_file(kline_filepath)

        # 读取订单数据  
        order_filepath = get_order_filepath(stock_code)
        order_content = read_file(order_filepath)

        # 读取真实交易数据
        gt_filepath = get_ground_truth_filepath(stock_code)
        gt_content = read_file(gt_filepath)

        # 加载 prompt 模板
        stg_path = get_strategy_filepath(f'{stg}')
        prompt_stg = read_file(stg_path)
        
        # 替换模板变量
        prompt = (prompt_stg
                 .replace('{STOCK_CODE}', stock_code)
                 .replace('{KLINE_DATA}', kline_content)
                 .replace('{ORDER_DATA}', order_content)
                 .replace('{GT_DATA}', gt_content))

        # 保存提示语
        stock_prompt_path = os.path.join('prompts', f'{stock_code}_prompt.txt')
        write_file(stock_prompt_path, prompt)
        
        print_success(stock_code, stock_prompt_path, "提示语")
        
    except Exception as e:
        print(f"✗ {stock_code} 构建提示语失败: {str(e)}")

def main():
    stock_code = 'HK.00700'
    build_stock_prompt(stock_code, stg='stg02') 

    stock_code = 'HK.09988'
    build_stock_prompt(stock_code, stg='stg02')    

if __name__ == "__main__":
    main()
