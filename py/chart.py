import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt 

def chart():
    ma1=input("ma1:")
    ma2=input("ma2:")
    MA1=int(ma1)
    MA2=int(ma2)
    name=input("Input Ticker:")
    print(name)
    df = yf.download(name,start="2019-1-1")
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
    plt.figure(figsize=(12,5))
    plt.plot(df['Adj Close'],label="stock price",c="blue",alpha=1.2)
    plt.plot(df[ma1],label="MA"+ma1,c="k",alpha=0.9)
    plt.plot(df[ma2],label="MA"+ma2,c="magenta",alpha=0.9)
    plt.scatter(df.iloc[buy].index,df.iloc[buy]["Adj Close"],marker="^",color="g",s=100)
    plt.scatter(df.iloc[sell].index,df.iloc[sell]["Adj Close"],marker="v",color="r",s=100)
    plt.legend()
    
    return plt.show()

chart()