import streamlit as st
import pandas as pd
import yfinance as yf

def news_page(tickers):
    st.title('Latest News')

    stock = st.selectbox('Select a company', tickers, key='news select')
    ticker = yf.Ticker(stock)

    def get_news_headers(news):
        for article in news:
            st.write(f"[{article['title']}]({article['link']})")
            

    if len(stock) > 0:
        st.subheader(f'{stock} Latest News!')
        with st.spinner('Loading News...'):
            get_news_headers(ticker.news)
            st.write(ticker)