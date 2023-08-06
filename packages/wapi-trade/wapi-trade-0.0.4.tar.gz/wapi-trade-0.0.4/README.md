# wapi
wapi is an open source library that acts as a Wealthsimple Trade API wrapper for python. 

## Installation
    pip install wapi-trade

## Functions
wapi can be used to place both market and limit orders, return available account balance, return information on current positions being held, return order information and much more.

## Example Usage
    from wapi import Trade
    import sys
    
    symbol = "SU"
    
    trade = Trade("email", "password")
    
    account_balance = trade.get_account_balance("tfsa")["buying_power"]
    position = trade.get_position()
    
    suncor_price = trade.get_market_value(trade.get_security_id(symbol))
    
    if account_balance > suncor_price and symbol not in position:
        order_id = trade.place_market_order(symbol, "buy", "tfsa", 1)
    else:
        print("Did not buy")
        sys.exit()
        
    order_info = trade.get_order(order_id)
    
    print(order_info)
 
