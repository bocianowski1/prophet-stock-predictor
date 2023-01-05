import streamlit as st
from datetime import date
import pandas as pd
import numpy as np
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs

from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page


st.title('Predict Stock Price')
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
    default_index=1,
    orientation='horizontal',
)

for key, value in pages.items():
    if selected_page == key and selected_page != 'Predict':
        switch_page(value)


tickers = pd.read_csv('data/marketcap.csv')
tickers['Both'] = tickers['Ticker'] + ' - ' + tickers['Name']

selected_stock = st.selectbox('Select a company', tickers['Both'], key='predict select')
selected_stock = selected_stock.split(' ')[0]

with st.expander('Ticker not in the list?'):
    new_ticker = st.text_input('Ticker', key='new ticker to predict')

def all_zero_columns(df: pd.DataFrame, col: str) -> bool:
    return np.all(df[col] == 0.0)

start_date_col, end_date_col = st.columns(2)
start_date = start_date_col.date_input('Start Date', value=date(2015, 1, 1), key='predict start')
end_date = end_date_col.date_input('End Date', value=date.today(), key='predict end')

@st.cache
def get_stock(ticker) -> pd.DataFrame:
    data: pd.DataFrame = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data


if len(new_ticker) > 0:
    stock = get_stock(new_ticker)['Close']
    if len(stock) > 0:
        selected_stock = new_ticker
    else:
        st.warning(f'{new_ticker} does not exist')
    

with st.spinner('Fetching Stock Data'):
    data = get_stock(selected_stock)

def plot_data(data):
    fig = graph_objs.Figure()
    fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Open'], name='Opening Price'))
    fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Close'], name='Closing Price'))
    fig.layout.update(title_text=f"{selected_stock.upper()}'s Opening/Closing Price", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

with st.expander('Show Opening/Closing Price'):
    plot_data(data)

train_data = data[['Date', 'Close']]
train_data = train_data.rename(columns={
    'Date': 'ds',
    'Close': 'y'
})

model = Prophet()
model.fit(train_data)

st.subheader(f'Forecast for {selected_stock.upper()}')
num_years = st.slider('Years of prediction', 1, 5)
period = num_years * 365
predicted_data = model.make_future_dataframe(periods=period)

with st.spinner('Loading Prediction'):
    prediction = model.predict(predicted_data)

prediction_figure1 = plot_plotly(model, prediction, xlabel='Year', ylabel='Price in USD')
st.plotly_chart(prediction_figure1, use_container_width=True)

if st.button('Show Forecast Components'):
    st.subheader(f'Forecast Components for {selected_stock}')
    prediction_figure2 = model.plot_components(prediction)
    st.write(prediction_figure2)

