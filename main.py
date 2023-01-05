import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
from plotly import graph_objs

from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

st.title('S&P 500 Stock Dashboard')
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
    default_index=0,
    orientation='horizontal'
)

for key, value in pages.items():
    if selected_page == key and selected_page != 'Home':
        switch_page(value)

tickers = pd.read_csv('data/marketcap.csv')
tickers['Both'] = tickers['Ticker'] + ' - ' + tickers['Name']

def get_stock(ticker) -> pd.DataFrame:
    data: pd.DataFrame = yf.download(ticker, date(2018, 12, 1), date.today())
    data.reset_index(inplace=True)
    return data

def name_from(ticker: str) -> str:
    ticker = ticker.upper()
    try:
        name: str = tickers.loc[tickers['Ticker'] == ticker].iloc[0]['Name']
        if len(name) > 15:
            return name.split(' ')[0]
        else:
            return name

    except:
        return ticker


col1, col2 = st.columns([1, 2])
col1.subheader('Predict and Analyze Future Stock Prices')
col1.write("""
    Predict the future closing price of an S&P 500 listed 
    stock using the FaceBook [Prophet]('https://facebook.github.io/prophet/'). 
    Adjust the forecast duration and examine the forecast components.
""")
ticker = 'AAPL'
data = get_stock(ticker)

def plot_closing_price(data, ticker, height):
    fig = graph_objs.Figure()
    fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Close'], name='Closing Price'))
    fig.layout.update(title_text=f"{ticker.upper()}'s Closing Price", xaxis_rangeslider_visible=True)
    fig.update_layout(height=height)
    col2.plotly_chart(fig, use_container_width=True)
col2.subheader(f'Example: {name_from(ticker)}')
plot_closing_price(data, ticker, 400)
# prediction_figure1 = plot_plotly(model, prediction, xlabel='Year', ylabel='Price in USD', figsize=(300, 400))
# col2.plotly_chart(prediction_figure1, use_container_width=True)


col1, col2 = st.columns([1, 2])
col1.subheader("Visualize and Compare the Behavoir Stocks")
col1.markdown("""
    Compare multiple S&P 500 stocks with beautiful, interactive [plotly]('https://plotly.com/') graphs. 
    Add companies several companies and choose the time interval.
""")



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
def get_stocks(stocks) -> pd.DataFrame:
    data = cumulative_returns(
        yf.download(stocks, date(2018, 12, 1), date.today())
    )
    return data


def plot_data(streamlit: st, stocks: pd.DataFrame, selected_stocks: list, height: int=600):
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

    if height:
        fig.update_layout(height=height)
    streamlit.plotly_chart(fig, use_container_width=True)

example_stocks = ['MSFT', 'TSLA']
col2.subheader(f'Example: {name_from(example_stocks[0])} vs {name_from(example_stocks[1])}')
example_data = get_stocks(example_stocks)
plot_data(col2, example_data, example_stocks, height=400)


col1, col2 = st.columns([1, 2])
col1.subheader("Get the Latest News and Financial Analytics")
col1.write("""
    Retrieve insightful information i.e. the cash flow of a company of your choice 
    and the latest news regarding a given company from [Yahoo Finance]('https://finance.yahoo.com/').
""")

ticker = yf.Ticker('GOOG')
col2.subheader(f'Latest News Example: {name_from("GOOG")}')
col2.write('')
for i in range(3):
    col2.markdown(f"[{ticker.news[i]['title']}]({ticker.news[i]['link']})")

st.caption('Created by Torger Bocianowski')

