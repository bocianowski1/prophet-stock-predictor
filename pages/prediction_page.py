import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs


def prediction_page():
    stocks = ('AAPL', 'GOOG', 'MSFT')
    selected_stock = st.selectbox('Choose a Stock', stocks)

    # if st.button('Ticker not present in list'):
    #     new_ticker = st.text_input('Ticker')
    #     st.write(f'{new_ticker}')

    start_date_col, end_date_col = st.columns(2)
    start_date = start_date_col.date_input('Start Date', value=date(2015, 1, 1), key=1)
    end_date = end_date_col.date_input('End Date', value=date.today(), key=2)


    @st.cache 
    def get_stock(ticker) -> pd.DataFrame:
        data = yf.download(ticker, start_date, end_date)
        data.reset_index(inplace=True)
        return data

    with st.spinner('Fetching Stock Data🤑'):
        data = get_stock(selected_stock)
    # st.success(f'Fetched {selected_stock}')

    # st.subheader('Raw Data')
    # st.write(data.tail())

    def plot_raw_data():
        fig = graph_objs.Figure()
        fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Open'], name='Opening Price'))
        fig.add_trace(graph_objs.Scatter(x=data['Date'], y=data['Close'], name='Closing Price'))
        fig.layout.update(title_text='Time Series Data', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    train_data = data[['Date', 'Close']]
    train_data = train_data.rename(columns={
        'Date': 'ds',
        'Close': 'y'
    })

    model = Prophet()
    model.fit(train_data)

    n_years = st.slider('Years of prediction', 1, 4)
    period = n_years * 365
    predicted_data = model.make_future_dataframe(periods=period)
    # prediction = model.predict(predicted_data)

    with st.spinner('Loading Prediction💭'):
        prediction = model.predict(predicted_data)
    st.subheader('Prediction')
    st.write(prediction.tail())