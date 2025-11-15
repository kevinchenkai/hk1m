import os
import pandas as pd
from datetime import datetime
from futu import *

# 公共股票代码列表
STOCK_CODES = [
    'HK.00700',  # 腾讯控股
    'HK.01024',  # 快手-W
    'HK.03690',  # 美团-W
    'HK.09988',  # 阿里巴巴-W
    'HK.01810',  # 小米集团-W
    'HK.00981',  # 中芯国际
    'HK.800000', # 恒生指数
    'HK.800700'  # 恒生科技指数
]

# 公共配置
DEFAULT_DATA_DIR = './datasets'
DEFAULT_KLINES_DIR = './datasets/klines'
DEFAULT_ORDERS_DIR = './datasets/orders'
DEFAULT_GROUND_DIR = './datasets/ground'
DEFAULT_PROMPTS_DIR = './prompts'
DEFAULT_LOGS_DIR = './logs'

# 文件操作公共函数
def write_file(filepath, content):
    """
    写入文件内容
    
    Args:
        filepath (str): 文件路径
        content (str): 文件内容
    
    Raises:
        IOError: 写入文件时出错
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        raise IOError(f"写入文件时出错: {str(e)}")

def read_file(filepath):
    """
    读取文件内容
    
    Args:
        filepath (str): 文件路径
    
    Returns:
        str: 文件内容
    
    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取文件时出错
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().strip()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")
    except Exception as e:
        raise IOError(f"读取文件时出错: {str(e)}")

# 路径生成公共函数
def get_data_dir(stock_code, data_dir=DEFAULT_DATA_DIR):
    """
    生成数据目录路径
    
    Args:
        stock_code (str): 股票代码
        data_dir (str): 基础数据目录
    
    Returns:
        str: 完整数据目录路径
    """
    sub_dir = stock_code.split('.')[0]
    month = datetime.now().strftime('%Y%m')
    full_dir = os.path.join(data_dir, sub_dir, month)
    return full_dir

def ensure_dir_exists(dir_path):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        dir_path (str): 目录路径
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_kline_filepath(stock_code, data_dir=DEFAULT_KLINES_DIR):
    """
    生成K线数据文件路径
    
    Args:
        stock_code (str): 股票代码
        data_dir (str): K线数据目录
    
    Returns:
        str: K线数据文件路径
    """
    full_dir = get_data_dir(stock_code, data_dir)
    today = datetime.now().strftime('%y%m%d')
    filename = f"{stock_code}_{today}.jsonl"
    filepath = os.path.join(full_dir, filename)
    return filepath

def get_order_filepath(stock_code, data_dir=DEFAULT_ORDERS_DIR):
    """
    生成订单数据文件路径
    
    Args:
        stock_code (str): 股票代码
        data_dir (str): 订单数据目录
    
    Returns:
        str: 订单数据文件路径
    """
    full_dir = get_data_dir(stock_code, data_dir)
    filename = f"{stock_code}_order.jsonl"
    filepath = os.path.join(full_dir, filename)
    return filepath

def get_ground_truth_filepath(stock_code, data_dir=DEFAULT_GROUND_DIR):
    """
    生成真实交易数据文件路径
    
    Args:
        stock_code (str): 股票代码
        data_dir (str): 真实数据目录
    
    Returns:
        str: 真实交易数据文件路径
    """
    filename = f"{stock_code}_gt.jsonl"
    filepath = os.path.join(data_dir, filename)
    return filepath

# 数据保存公共函数
def save_data_to_jsonl(data, filepath, columns_to_keep=None, date_columns=None):
    """
    保存数据到JSONL文件
    
    Args:
        data (pd.DataFrame): 要保存的数据
        filepath (str): 文件路径
        columns_to_keep (list): 要保留的列名列表
        date_columns (list): 需要格式化为日期的列名列表
    """
    # 确保目录存在
    ensure_dir_exists(os.path.dirname(filepath))

    # 创建数据副本以避免SettingWithCopyWarning
    data = data.copy()
    
    # 如果指定了要保留的列，则过滤
    if columns_to_keep:
        data = data[columns_to_keep]
    
    # 处理日期列
    if date_columns:
        for col in date_columns:
            if col in data.columns:
                data[col] = pd.to_datetime(data[col]).dt.strftime('%Y-%m-%d')
    
    # 保存数据
    data.to_json(filepath, orient='records', lines=True, force_ascii=False)

# 打印公共函数
def print_success(stock_code, filepath, data_type="数据"):
    """
    打印成功消息
    
    Args:
        stock_code (str): 股票代码
        filepath (str): 文件路径
        data_type (str): 数据类型描述
    """
    print(f"✓ {stock_code} {data_type}已保存到: {filepath}")

def print_error(stock_code, error_msg, data_type="数据"):
    """
    打印错误消息
    
    Args:
        stock_code (str): 股票代码
        error_msg (str): 错误消息
        data_type (str): 数据类型描述
    """
    print(f"✗ {stock_code} {data_type}获取失败: {error_msg}")

# Futu API 公共函数
def create_quote_context(host='127.0.0.1', port=11111):
    """
    创建行情上下文
    
    Args:
        host (str): 主机地址
        port (int): 端口号
    
    Returns:
        OpenQuoteContext: 行情上下文对象
    """
    return OpenQuoteContext(host=host, port=port)

def create_trade_context(host='127.0.0.1', port=11111):
    """
    创建交易上下文
    
    Args:
        host (str): 主机地址
        port (int): 端口号
    
    Returns:
        OpenSecTradeContext: 交易上下文对象
    """
    return OpenSecTradeContext(
        filter_trdmarket=TrdMarket.HK,
        host=host,
        port=port,
        security_firm=SecurityFirm.FUTUSECURITIES
    )

def format_date_range(days):
    """
    生成日期范围
    
    Args:
        days (int): 天数
    
    Returns:
        tuple: (开始日期, 结束日期)
    """
    from datetime import timedelta
    
    p_end = datetime.now().strftime('%Y-%m-%d')
    p_start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    return p_start, p_end
