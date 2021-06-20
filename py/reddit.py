import config
import psycopg2
import psycopg2.extras
import config
from dotenv import load_dotenv
import os

load_dotenv()
# 取得comment ratio on reddit
def rate():
    # connection = psycopg2.connect(host=os.getenv.DB_HOST, database=os.getenv.DB_NAME, user=os.getenv.DB_USER, password=os.getenv.DB_PASS)
    connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(""" 
        select count(*) as num_mentions , symbol from mention join stock on stock.id = mention.stock_id group by stock_id , symbol order by num_mentions DESC limit 10; 
    """)
    stock_symbol = cursor.fetchall()
    vote_list=[]
    symbol_list=[]
    for i in stock_symbol:
        vote=i[0]
        symbol=i[1]
        vote_list.append(vote)
        symbol_list.append(symbol)
    sum=0
    for index in range(len(stock_symbol)):
        count=vote_list[index]
        sum=sum+count
    ratio=[]
    for j in vote_list:
        ratio.append(j/sum*100) 
    # return ratio,symbol_list
    dic={}
    for i in range(10):
        dic.setdefault("symbol",[])
        dic.setdefault("ratio",[])
        dic["symbol"].append(symbol_list[i])
        dic["ratio"].append(ratio[i])

    return dic

