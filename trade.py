# 執行order

from tda import auth, client
import tda
from tda.orders.equities import *
from tda.orders.common import Duration, Session
import json
import config
import datetime
from tda.orders.common import OrderType
from tda.orders.generic import OrderBuilder


# authenticate
try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)
# print(json.dumps(c.get_quote("AAPL").json(),indent=4))
# response = c.search_instruments("AAPL", c.Instrument.Projection.FUNDAMENTAL)
# print(json.dumps(response.json(), indent=4))

watchlist=["PLTR","GOLD"]
fundamental= c.search_instruments(watchlist, c.Instrument.Projection.FUNDAMENTAL)
for name in watchlist:
    market=c.get_quote(name)
    marketInfo=market.json()
    print("---")
    print(marketInfo[name]["symbol"],":",marketInfo[name]["mark"])
    order_limit = tda.orders.equities.equity_buy_limit(name, price=1,quantity=1)
    # order_market=tda.orders.equities.equity_buy_market(name,quantity=1)
    r = c.place_order(config.account_id, order_limit)
    if r : 
        print("order filled : "+f'{name}')


    # print("取得52周high:",fundamental.json()[name]["fundamental"]["high52"] )
    # print("peRatio",fundamental.json()[name]["fundamental"]["peRatio"])
    # print("距離前高ratio:",marketInfo[name]["mark"]/fundamental.json()[name]["fundamental"]["high52"] )
    # order_market=tda.orders.equities.equity_buy_market("MA",quantity=1)







# # get option chain
# response = c.get_option_chain('AAPL')
# print("3.取得選擇權資料")
# print(json.dumps(response.json(), indent=4))


# # get all call options
# response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL)
# print("4.取得所有選擇權資料")
# print(json.dumps(response.json(), indent=4))


# # get call options for a specific strike
# response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL, strike=130t)
# print("4.取得特定執行價格選擇權資料")
# print(json.dumps(response.json(), indent=4))

# # get call options for a specific strike and date range
# start_date = datetime.datetime.strptime('2020-04-24', '%Y-%m-%d').date()
# end_date = datetime.datetime.strptime('2020-05-01', '%Y-%m-%d').date()

# response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL, strike=300, strike_from_date=start_date, strike_to_date=end_date)

# print(json.dumps(response.json(), indent=4))


# # limit order of 5 shares of redfin stock at 18 dollars a share

# stock="PLTR"
# order_limit = tda.orders.equities.equity_buy_limit("PLTR", price=1,quantity=1)
# # order_market=tda.orders.equities.equity_buy_market("MA",quantity=1)


# r = c.place_order(config.account_id, order_limit)
# if r : 
#     print("order filled : "+f'{stock}')



# builder = OrderBuilder
# # builder.set_instruction(OrderBuilder.Instruction.BUY)
# builder.set_order_type(OrderBuilder.orderType.LIMIT)
# builder.set_price(18)

# builder.set_duration(Duration.GOOD_TILL_CANCEL)
# builder.set_session(Session.NORMAL)

# response = c.place_order(config.account_id, builder.build())

# print(response)

# get price history for a symbol
# r = c.get_price_history('AAPL',
#         period_type=client.Client.PriceHistory.PeriodType.YEAR,
#         period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#         frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#         frequency=client.Client.PriceHistory.Frequency.DAILY)
# print(json.dumps(r.json(), indent=4))

