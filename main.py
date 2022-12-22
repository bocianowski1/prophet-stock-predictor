import streamlit as st
import pandas as pd

from pages.prediction_page import prediction_page
from pages.compare_page import compare_page
from pages.news_page import news_page
from pages.info_page import info_page
from pages.about_page import about_page

tickers = pd.read_csv('data/marketcap.csv')['Ticker']

st.title('S&P 500 Stock Dashboard')
tabs_list = [
    'Predict Future Price',
    'Additional Info',
    'Comapare',
    'Latest News',
    'About this Project'
    ]
tabs = st.tabs(tabs_list)

with tabs[0]:
    prediction_page(tickers)

with tabs[1]:
    info_page(tickers)

with tabs[2]:
    compare_page(tickers)

with tabs[3]:
    news_page(tickers)

with tabs[4]:
    about_page()
