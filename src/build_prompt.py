import os
from datetime import datetime

def write_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        raise IOError(f"写入文件时出错: {str(e)}")

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")
    except Exception as e:
        raise IOError(f"读取文件时出错: {str(e)}")

def build_stock_prompt(stock_code, data_dir='./data', stg=1):
    sub_dir = stock_code.split('.')[0]
    month = datetime.now().strftime('%Y%m')
    full_dir = os.path.join(data_dir, sub_dir, month)

    # 读取K线数据
    kline_path = f"{stock_code}_{datetime.now().strftime('%y%m%d')}.jsonl"
    filepath = os.path.join(full_dir, kline_path)
    kline_content = read_file(filepath)

    # 读取订单数据
    order_path = f"{stock_code}_order.jsonl"
    filepath = os.path.join(full_dir, order_path)
    order_content = read_file(filepath)

    # 读取真实交易数据
    gt_path = f"{stock_code}_gt.jsonl"
    filepath = os.path.join(full_dir, gt_path)
    gt_content = read_file(filepath)

    # 加载 prompt 模板
    prompt_path = os.path.join('prompts', f'prompt_stg{stg}.template')
    prompt_content = read_file(prompt_path)
    prompt = prompt_content.replace('{STOCK_CODE}', stock_code).replace('{KLINE_DATA}', kline_content).replace('{ORDER_DATA}', order_content).replace('{GT_DATA}', gt_content)

    stock_prompt = os.path.join('prompts', f'{stock_code}_prompt.txt')
    write_file(stock_prompt, prompt)

    #print(prompt)
    # 构建提示语
    print(f"✓ {stock_code} 提示语已保存到: {stock_prompt}")

def main():
    stock_code = 'HK.00700'
    build_stock_prompt(stock_code, stg=2) 

    stock_code = 'HK.09988'
    build_stock_prompt(stock_code, stg=2)    

# 使用示例
if __name__ == "__main__":
    main()

"""
# Run:
1. python getKLines.py  #获取 64天 K线数据
2. python getOrder.py #获取 60天 订单数据
3. python buildPrompt.py #构建提示语
"""