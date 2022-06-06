import streamlit as st
import plotly.express as px
import yfinance as yf
import pandas as pd

st.set_page_config(
        page_title="Stock APP",
        page_icon="chart_with_upwards_trend",
        layout="wide")
st.sidebar.image("https://www.investopedia.com/thmb/4RO3l7ItujBm2G_TgQJe6rs-Hms=/2224x1348/filters:fill(auto,1)/stock-exchange-graph-and-numbers-926129268-269a9dde59e74a9caa768eaa0f260b46.jpg")
def create_graph(stockdata,period,value):   
    fig = px.line(stockdata, y=value, title=stocksymbol)
    fig.update_layout(xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

stocksymbol=st.text_input("stock symbol")    
period=st.selectbox("period selection",("1d","max","ytd","1mo","6mo","1y","2y"))
stockdata = yf.Ticker(stocksymbol).history(period=period)
currency=yf.Ticker("USDEUR=X").history(period=period)
selected_currency=st.radio("Currency", ["USD", "EUR", "BOTH"],horizontal=True)
stockdata['EurRate'] = stockdata.index.map(currency["Close"])
stockdata['CloseEurRate']=stockdata['Close']*stockdata['EurRate']


if stocksymbol != "" :
    if selected_currency=="EUR":
        create_graph(stockdata,period,"CloseEurRate")
    elif selected_currency=="USD":
        create_graph(stockdata,period,"Close")
    elif selected_currency=="BOTH":
        delta=stockdata['Close'].iloc[0]-stockdata['CloseEurRate'].iloc[0]
        stockdata['CloseRel']=stockdata['Close']-delta
        create_graph(stockdata,period,["CloseEurRate","CloseRel"])
