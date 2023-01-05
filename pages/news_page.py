import streamlit as st
import pandas as pd
import yfinance as yf

from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

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

def get_news_headers(news):
    for article in news:
        col1, col2 = st.columns(2)
        try:
            img = article['thumbnail']['resolutions'][0]['url']
            col1.image(img, use_column_width=True)
        except:
            col1.text('No image')
        col2.subheader(f"[{article['title']}]({article['link']})")            

if len(stock) > 0:
    with st.spinner('Loading News...'):
        get_news_headers(ticker.news)