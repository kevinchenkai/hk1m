import os
from datetime import datetime
from common import *

START_DAY = '20251001'

def build_stock_prompt():
    """
    构建股票提示语
    
    Args:
        stock_code (str): 股票代码
        stg (int): 阶段，默认1
    """
    try:
        #计算今天与起始时间的天数差
        today = datetime.now().strftime('%Y%m%d')
        day = (datetime.now() - datetime.strptime(START_DAY, '%Y%m%d')).days

        # 获取投资组合内容
        portfolio_content = calculate_portfolio()

        # 读取最新K线数据
        stock_code = 'HK.00700'
        kline_filepath = get_kline_lastest(stock_code)
        kline_content = read_file(kline_filepath)

        stock_code = 'HK.09988'
        kline_filepath = get_kline_lastest(stock_code)
        kline_content = kline_content + '\n' +read_file(kline_filepath)

        # 读取订单数据
        stock_code = 'HK.00700'
        order_filepath = get_order_filepath(stock_code)
        order_content = read_file(order_filepath)
        stock_code = 'HK.09988'
        order_filepath = get_order_filepath(stock_code)
        order_content = order_content + '\n' + read_file(order_filepath)

        # 读取真实交易数据
        gt_content_list = []
        stock_code = 'HK.00700'
        gt_content_list.extend(read_ground_truth_data(stock_code, filter_date=START_DAY))
        stock_code = 'HK.09988'
        gt_content_list.extend(read_ground_truth_data(stock_code, filter_date=START_DAY))
        gt_content = '\n'.join(gt_content_list)
        
        # 加载 prompt 模板
        stg_path = get_strategy_filepath(f'stg03')
        prompt_stg = read_file(stg_path)
        
        # 替换模板变量
        prompt = (prompt_stg
                .replace('{START_DAY}', START_DAY)
                .replace('{TODAY}', today)
                .replace('{DAY}', str(day))
                .replace('{PORTFOLIO}', portfolio_content)
                .replace('{STOCK_CODE}', stock_code)
                .replace('{KLINE_DATA}', kline_content)
                .replace('{ORDER_DATA}', order_content)
                .replace('{GT_DATA}', gt_content))

        # 保存提示语
        stock_prompt_path = os.path.join('prompts', f'combined_prompt.txt')
        write_file(stock_prompt_path, prompt)
        
        print_success(stock_code, stock_prompt_path, "提示语")
        
    except Exception as e:
        print(f"✗ {stock_code} 构建提示语失败: {str(e)}")

def main():
    # 构建股票提示语
    build_stock_prompt() 

if __name__ == "__main__":
    main()
