import json
from datetime import datetime
from common import *

def calculate_portfolio():
    """
    根据真实交易数据计算当前资金和持仓
    
    初始状态:
    - 资金: 1,000,000
    - HK.00700: 1,000 股
    - HK.09988: 2,000 股
    
    Returns:
        str: 包含所有计算信息的字符串
    """
    content = []
    
    # 初始状态
    initial_cash = 1000000
    initial_holdings = {
        'HK.00700': 1000,
        'HK.09988': 2000
    }
    
    cash = initial_cash
    holdings = initial_holdings.copy()
    
    # 读取订单数据
    orders = []
    order_errors = []
    for stock_code in ['HK.00700', 'HK.09988']:
        order_filepath = get_order_filepath(stock_code)
        try:
            with open(order_filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    order = json.loads(line.strip())
                    if order['order_status'] == 'FILLED_ALL':
                        orders.append(order)
        except Exception as e:
            order_errors.append(f"读取 {stock_code} 订单数据失败: {str(e)}")
    
    # 按日期排序
    orders.sort(key=lambda x: datetime.strptime(x['create_time'], '%Y-%m-%d'))
    
    # 处理每笔成交订单
    trade_records = []
    for order in orders:
        date = order['create_time']
        code = order['code']
        side = order['trd_side']
        price = order['price']
        qty = order['qty']
        
        if side == 'BUY':
            cost = price * qty
            cash -= cost
            holdings[code] += qty
            trade_records.append(f"{date} | {code} | 买入 {int(qty)} 股 @ {price} | 成本: {cost:,.2f}")
        else:  # SELL
            proceeds = price * qty
            cash += proceeds
            holdings[code] -= qty
            trade_records.append(f"{date} | {code} | 卖出 {int(qty)} 股 @ {price} | 收入: {proceeds:,.2f}")
    
    # 按顺序输出：初始状态，当前状态，成交记录
    content.append("初始状态:")
    content.append(f"现金: {initial_cash:,.2f} HKD")
    content.append(f"HK.00700: {initial_holdings['HK.00700']} 股")
    content.append(f"HK.09988: {initial_holdings['HK.09988']} 股")
    content.append("")

    content.append("当前状态:")
    content.append(f"现金: {cash:,.2f} HKD")
    content.append(f"HK.00700: {int(holdings['HK.00700'])} 股")
    content.append(f"HK.09988: {int(holdings['HK.09988'])} 股")
    content.append("")
    
    content.append("成交记录:")
    content.append("-" * 60)

    if trade_records:
        content.extend(trade_records)
    content.append("-" * 60)
    
    return '\n'.join(content)

def main():
    result = calculate_portfolio()
    print(result)

if __name__ == "__main__":
    main()