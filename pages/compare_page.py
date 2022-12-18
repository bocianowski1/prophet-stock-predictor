import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs

def compare_page():
    stocks = ('AAPL', 'GOOG', 'MSFT')
    stocks_compare = st.multiselect('Choose a Stock', stocks)
    
    new_ticker = st.text_input('Ticker')
    if len(new_ticker) > 0:
        stocks_compare.append(new_ticker)

    start_date_col, end_date_col = st.columns(2)
    start_date = start_date_col.date_input('Start Date', value=date(2015, 1, 1), key=3)
    end_date = end_date_col.date_input('End Date', value=date.today(), key=4)

    if len(stocks_compare) > 0:
        pass

