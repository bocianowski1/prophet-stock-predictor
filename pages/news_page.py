import streamlit as st
import pandas as pd
import yfinance as yf

def news_page():
    st.title('News')

    stock = st.text_input('Ticker', key='news stock')
    ticker = yf.Ticker(stock)

    def get_news_headers(news):
        for article in news:
            st.write(f"{article['title']} [link]({article['link']})")
            

    if len(stock) > 0:
        st.subheader(f'{stock.upper()} Latest News!')
        with st.spinner('Loading News...📰'):
            get_news_headers(ticker.news)