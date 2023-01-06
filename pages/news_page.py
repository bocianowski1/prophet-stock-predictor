import streamlit as st
import pandas as pd
import yfinance as yf

from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space

st.title('Latest News')
pages = {
    'Home': 'main',
    'Predict': 'prediction_page',
    'Compare': 'compare_page',
    'Info': 'info_page',
    'News': 'news_page'
}

selected_page = option_menu(
    menu_title=None,
    icons=['house', 'piggy-bank', 'search', 'info-circle', 'newspaper'],
    options=list(pages.keys()),
    default_index=4,
    orientation='horizontal'
)

for key, value in pages.items():
    if selected_page == key and selected_page != 'News':
        switch_page(value)

tickers = pd.read_csv('data/marketcap.csv')
tickers['Both'] = tickers['Ticker'] + ' - ' + tickers['Name']


stock = st.selectbox('Select a company', tickers['Both'], key='news select')
stock = stock.split(' ')[0]
ticker = yf.Ticker(stock)

def get_news_headers(st: st, news: list):
    col1, col2 = st.columns(2)
    
    for i in range(len(news)):
        article = news[i]
        if i % 2 == 0:
            st = col1
        else: st = col2

        st.markdown("<a href="f'{article["link"]}'" target='_blank' style='font-size: 20px; text-decoration: none;'>"f'{article["title"]}'"</a>", unsafe_allow_html=True)
        try:
            img = article['thumbnail']['resolutions'][0]['url']
            st.image(img, width=300)
        except:
            st.text('No image😔')
        add_vertical_space(3)

if len(stock) > 0:
    with st.spinner('Loading News...'):
        get_news_headers(st, ticker.news)