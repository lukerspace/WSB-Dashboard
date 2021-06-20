import sys
from matplotlib import markers
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 
from reddit import *

vote=rate()
def chart(name):
    # ma1=input("ma1:")
    # ma2=input("ma2:")
    ma1="20"
    ma2="50"
    MA1=int(ma1)
    MA2=int(ma2)
    # name=input("Input Ticker:")
    df = yf.download(name,start="2020-1-1")
    df[ma1]=df["Adj Close"].rolling(MA1).mean()
    df[ma2]=df["Adj Close"].rolling(MA2).mean()
    df=df[["Adj Close",ma1,ma2]]
    df=df.dropna()
    buy=[]
    sell=[]
    for i in range(len(df)):
        if df[ma1].iloc[i]>df[ma2].iloc[i] and df[ma1].iloc[i-1]<df[ma2].iloc[i-1]:
            buy.append(i)
        elif df[ma1].iloc[i]<df[ma2].iloc[i] and df[ma1].iloc[i-1]>df[ma2].iloc[i-1]:
            sell.append(i)
    plt.style.use("dark_background")
    plt.figure(figsize=(10,5))
    plt.grid(linestyle='-', linewidth=0.1,data=(10,10))
    plt.plot(df['Adj Close'],label="stock price",c="orange",alpha=50)
    plt.plot(df[ma1],label="MA"+ma1,c="white",alpha=5)
    plt.plot(df[ma2],label="MA"+ma2,c="skyblue",alpha=5)
    plt.scatter(df.iloc[buy].index,df.iloc[buy]["Adj Close"],marker="^",color="green",s=40,zorder=10)
    plt.scatter(df.iloc[sell].index,df.iloc[sell]["Adj Close"],marker="v",color="red",s=40,zorder=10)
    plt.legend(fontsize=8)
    plt.show(block=False)
    
    return input("press enter to exit")
# # 圖片瀏覽
def showchart():
    for i in range(10):
        print(vote["symbol"][i])
        img=chart(vote["symbol"][i])
    return img

showchart()


