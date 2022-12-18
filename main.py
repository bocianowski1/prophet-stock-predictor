import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs

from pages.prediction_page import prediction_page
from pages.compare_page import compare_page


st.title('Stock Dashboard')
tabs_list = [
    'Predict Future Stock Price',
    'Comapare Stocks'
    ]
tabs = st.tabs(tabs_list)

with tabs[0]:
    prediction_page()

with tabs[1]:
    compare_page()