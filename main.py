import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs

from pages.prediction_page import prediction_page
from pages.compare_page import compare_page
from pages.news_page import news_page
from pages.info_page import info_page


st.title('Stock Dashboard')
tabs_list = [
    'Predict Future Price',
    'Comapare',
    'Latest News',
    'Additional Info'
    ]
tabs = st.tabs(tabs_list)

with tabs[0]:
    prediction_page()

with tabs[1]:
    compare_page()

with tabs[2]:
    news_page()

with tabs[3]:
    info_page()

