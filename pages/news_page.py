import streamlit as st
import pandas as pd
import yfinance as yf

# def news_page(tickers: pd.DataFrame):
tickers = pd.read_csv('data/marketcap.csv')
st.title('Latest News')

stock = st.selectbox('Select a company', tickers['Ticker'], key='news select')
ticker = yf.Ticker(stock)

def get_news_headers(news):
    for article in news:
        col1, col2 = st.columns(2)
        try:
            img = article['thumbnail']['resolutions'][0]['url']
            col1.image(img, use_column_width=True)
        except:
            st.text('No image')
        col2.subheader(f"[{article['title']}]({article['link']})")            

if len(stock) > 0:
    with st.spinner('Loading News...'):
        get_news_headers(ticker.news)
        # st.write(ticker.news)