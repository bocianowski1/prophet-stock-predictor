import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs

def compare_page():
    st.title('Compare Stocks🔎')
    stocks = ('AAPL', 'GOOG', 'MSFT')
    selected_stocks = st.multiselect('Choose a Stock', stocks)
    
    new_ticker = st.text_input('Ticker')
    if len(new_ticker) > 0:
        selected_stocks.append(new_ticker)

    start_date_col, end_date_col = st.columns(2)
    start_date = start_date_col.date_input('Start Date', value=date(2015, 1, 1), key='compare start')
    end_date = end_date_col.date_input('End Date', value=date.today(), key='compare end')

    def get_stocks() -> pd.DataFrame:
        data = cumulative_returns(yf.download(selected_stocks, start_date, end_date)['Close'])
        # data.reset_index(inplace=True)
        return data

    def cumulative_returns(df: pd.DataFrame):
        relative = df.pct_change()
        cumulative = (1 + relative).cumprod() - 1
        cumulative = cumulative.fillna(0)
        return cumulative

    if len(selected_stocks) > 0:
        
        data = get_stocks()
        st.line_chart(data)

        

