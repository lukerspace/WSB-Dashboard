import alpaca_trade_api as tradeapi
import psycopg2,sys
import psycopg2.extras
sys.path.append("./config")
import config

connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select * from stock")
print(cursor.fetchall())


#### ALPACA INSERT THE DATA TO THE DATABASE ####

api = tradeapi.REST(config.API_KEY, config.API_SECRET, base_url=config.API_URL)
assets = api.list_assets()
for asset in assets:
    print(f"insert the stock {asset.name} {asset.symbol}")
    cursor.execute("""
        INSERT INTO stock (name, symbol, exchange, is_etf) 
        VALUES (%s, %s, %s, false)
    """, (asset.name, asset.symbol, asset.exchange))
connection.commit()
