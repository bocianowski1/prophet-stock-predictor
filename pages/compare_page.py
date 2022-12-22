import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs

def compare_page(tickers):
    st.title('Compare Stocks')
    selected_stocks = st.multiselect('Select companies to compare', tickers)
    
    with st.expander('Ticker not in the list?'):
        new_ticker = st.text_input('Ticker', key='new ticker to compare')

    if len(new_ticker) > 0:
        selected_stocks.append(new_ticker)

    start_date_col, end_date_col = st.columns(2)
    start_date = start_date_col.date_input('Start Date', value=date(2015, 1, 1), key='compare start')
    end_date = end_date_col.date_input('End Date', value=date.today(), key='compare end')

    
    def cumulative_returns(df: pd.DataFrame):
        relative = df.pct_change()
        cumulative = (1 + relative).cumprod() - 1
        cumulative = cumulative.fillna(0)
        return cumulative

    def get_stocks() -> pd.DataFrame:
        data = cumulative_returns(yf.download(selected_stocks, start_date, end_date))['Close']
        # data.reset_index(inplace=True)
        return data
    
    def plot_data(stocks: pd.DataFrame):
        fig = graph_objs.Figure()

        # print(f'\n\nType {(stocks)}\n')
        # print(f'LENGTH OF STOCKS {len(stocks)}')
        # for stock in stocks:
        #     print("HEYHEY", stock, type(stock))
        #     # fig.add_trace(graph_objs.Scatter(x=stock['Date'], y=stock['Close'], name='Closing Price'))

        # fig.add_trace(graph_objs.Scatter(x=stocks['Date'], y=stocks['Close'], name='Close Price'))
        # # fig.add_trace(graph_objs.Scatter(x=stocks['Date'], y=stocks['Close'], name='Closing Price'))
        fig.layout.update(title_text=f"Closing Price of {selected_stocks}", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    if len(selected_stocks) > 0:
        
        data = get_stocks()
        st.line_chart(data)
        

        

