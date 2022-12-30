import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
import numpy as np
from plotly import graph_objs

def compare_page(tickers: pd.DataFrame):
    st.title('Compare Stocks')
    selected_stocks = st.multiselect('Select companies to compare', tickers['Ticker'])
    
    with st.expander('Ticker not in the list?'):
        new_ticker = st.text_input('Ticker', key='new ticker to compare')

    if len(new_ticker) > 0:
        selected_stocks.append(new_ticker)

    col1, col2 = st.columns(2)
    start_date = col1.date_input('Start Date', value=date(2015, 1, 1), key='compare start')
    end_date = col2.date_input('End Date', value=date.today(), key='compare end')

    def name_from(ticker: str) -> str:
        ticker = ticker.upper()
        try:
            name: str = tickers.loc[tickers['Ticker'] == ticker].iloc[0]['Name']
            if len(name) > 15:
                return ticker
            else:
                return name
    
        except:
            return ticker

    def readable_from(ticker_list: list) -> str:
        if len(ticker_list) == 0:
            return ''
        return ''.join(name_from(ticker) + ', ' for ticker in ticker_list)[:-2]
    
    def all_zero_columns(df: pd.DataFrame, col: str) -> bool:
        return np.all(df[col] == 0.0)

    def cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
        relative = df.pct_change()
        cumulative = (1 + relative).cumprod() - 1
        cumulative = cumulative.fillna(0)
        return cumulative

    @st.cache
    def get_stocks() -> pd.DataFrame:
        data = cumulative_returns(
            yf.download(selected_stocks, start_date, end_date)
        )
        return data
    
    def plot_data(stocks: pd.DataFrame):
        fig = graph_objs.Figure()

        dates = stocks.reset_index()['Date']
        stocks = stocks['Close']
        gibberish_stocks = False

        if len(selected_stocks) == 1:
            fig.add_trace(graph_objs.Scatter(
                x=dates, y=stocks,
                name=readable_from(selected_stocks[0])
            ))
        else:
            for col in stocks:
                if not all_zero_columns(stocks, col):
                    fig.add_trace(graph_objs.Scatter(x=dates, y=stocks[col], name=name_from(col)))
                else:
                    gibberish_stocks = True

        fig.layout.update(title_text=
            f"Closing Price for: {readable_from(selected_stocks[:-1]) if gibberish_stocks else readable_from(selected_stocks)}",
            xaxis_rangeslider_visible=True
        )
        st.plotly_chart(fig)

    
    if len(selected_stocks) > 0:
        data = get_stocks()
        plot_data(data)
        # try:
        #     print('success')
        #     plot_data(data)
        # except:
        #     try:
        #         print('line chart')
        #         st.line_chart(data)
        #     except:
        #         st.text('There was an error visualizing the data.')
        

        

