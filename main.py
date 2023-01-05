import streamlit as st
import yfinance as yf

from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

from pages.prediction_page import model, plot_plotly, prediction
from pages.compare_page import get_stocks, plot_data

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


col1, col2 = st.columns([1, 2])
col1.subheader('Predict and Analyze Future Stock Prices')
col1.write("""
    Predict the future closing price of an S&P 500 listed 
    stock using the FaceBook [Prophet]('https://facebook.github.io/prophet/'). 
    Adjust the forecast duration and examine the forecast components.
""")
col2.subheader('Forecast for AAPL')
prediction_figure1 = plot_plotly(model, prediction, xlabel='Year', ylabel='Price in USD', figsize=(300, 400))
col2.plotly_chart(prediction_figure1, use_container_width=True)


col1, col2 = st.columns([1, 2])
col1.subheader("Visualize and Compare the Behavoir Stocks")
col1.markdown("""
    Compare multiple S&P 500 stocks with beautiful, interactive [plotly]('https://plotly.com/') graphs. 
    Add companies several companies and choose the time interval.
""")

example_stocks = ['MSFT', 'TSLA']
col2.subheader(f'{example_stocks[0]} vs {example_stocks[1]}')
example_data = get_stocks(example_stocks)
plot_data(col2, example_data, example_stocks, height=400, show_text=False)


col1, col2 = st.columns([1, 2])
col1.subheader("Get the Latest News and Financial Analytics")
col1.write("""
    Retrieve insightful information i.e. the cash flow of a company of your choice 
    and the latest news regarding a given company from [Yahoo Finance]('https://finance.yahoo.com/').
""")

ticker = yf.Ticker('GOOG')
col2.subheader(f'The Latest News for {"GOOG"}')
for i in range(3):
    col2.markdown(f"[{ticker.news[i]['title']}]({ticker.news[i]['link']})")

st.caption('Created by Torger Bocianowski')

