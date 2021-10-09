import os,sys
import streamlit as st
import pandas as pd
import numpy as np
import requests,tweepy
import psycopg2, psycopg2.extras
import plotly.graph_objects as go
from config import config

pre_path = os.path.abspath("../dashboard/py")
sys.path.append(pre_path)
# from reddit import *

# postgres
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

option = st.sidebar.selectbox("Which WSB Dashboard?", ('MENTION TIME', 'REDDICT MESSAGE', 'STOCKTWITS'), 0)

if option == 'MENTION TIME':
    st.header("WALLSTREETBETS - MENTION TIME")
    num_days = st.sidebar.slider('Within Past Few Days', 1, 120, 30)
    # ratio=reddict_rate()
    cursor.execute("""
        SELECT COUNT(*) AS num_mentions, symbol
        FROM mention JOIN stock ON stock.id = mention.stock_id
        WHERE date(dt) > current_date - interval '%s day'
        GROUP BY stock_id, symbol   
        HAVING COUNT(symbol) > 10
        ORDER BY num_mentions DESC
    """, (num_days,))

    mention_time = cursor.fetchall()
    sum=0
    st.subheader("Count the mention times in WSB.")
    for count in mention_time:
        sum+=1
        st.write("🚀",count[1]," : ",count[0]," times ")
        if sum==20:
            break
    st.subheader("Chart Image")
    symbol = st.sidebar.text_input("Image Symbol", value=mention_time[0][1], max_chars=8)
    st.image(f"https://finviz.com/chart.ashx?t={symbol}")

if option == 'STOCKTWITS':
    symbol = st.sidebar.text_input("Symbol", value='AAPL', max_chars=8)

    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json")

    data = r.json()

    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write("🚀"+message['body'])
        st.write("-------------------")

if option == 'REDDICT MESSAGE':
    st.header("WALLSTREETBETS - REDDICT MESSAGE")

    symbol = st.sidebar.text_input("Symbol", value='SDC', max_chars=8)
    symbol=symbol.upper()
    st.subheader(symbol)
    cursor.execute("""
        select symbol,dt,message 
        from mention join stock on stock.id=mention.stock_id
        where symbol=%s
        order by dt desc;
    """,(symbol,))

    reddict_msg = cursor.fetchall()
    for msg in reddict_msg:
        st.write(msg[1])
        st.write(msg[2])
        st.write("-------------------")

