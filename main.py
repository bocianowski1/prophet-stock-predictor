import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs
import time
# import markdown_strings as md


st.title('Stock Predictor')
# with st.sidebar:
#     st.tabs(['hey', 'yo'])
#     with st.spinner("Loading..."):
#         time.sleep(2)
#     st.success("Done!")

stocks = ('AAPL', 'GOOG', 'MSFT')
selected_stock = st.selectbox('Choose a Stock', stocks)

col1, col2 = st.columns(2)

# col1.subheader("Start Date")
start_date = col1.date_input('Start Date', value=date(2015, 1, 1))

end_date = col2.date_input('End Date', value=date.today())

n_years = st.slider('Years of prediction', 1, 4)

@st.cache 
def get_stock(ticker) -> pd.DataFrame:
    data = yf.download(ticker, start_date, end_date)
    data.reset_index(inplace=True)
    return data

with st.spinner('Fetching Stock Data🤑'):
    data = get_stock(selected_stock)
st.success(f'Fetched {selected_stock}')

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

period = n_years * 365
predicted_data = model.make_future_dataframe(periods=period)
# prediction = model.predict(predicted_data)

with st.spinner('Loading Prediction💭'):
    prediction = model.predict(predicted_data)
    st.subheader('Prediction')
    st.write(prediction.tail())