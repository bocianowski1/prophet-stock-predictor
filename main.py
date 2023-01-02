import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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



df = px.data.gapminder()
fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)
col1, col2 = st.columns([2, 1])
col1.plotly_chart(fig, use_container_width=True)
col2.subheader('Predict and Analyze Future Stock Prices')
col2.write("Predict the closing price of a stock from one of the S&P 500 listed or other populare companies. This is made possible by FaceBook's Prophet.")

col1, col2 = st.columns([1, 2])
col1.subheader("Visualize and Compare the Behavoir Stocks")
col1.write("Compare multiple S&P 500 stocks.")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])
col2.bar_chart(chart_data, use_container_width=True)

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

col1, col2 = st.columns([2, 1])
col1.map(df)
col2.subheader("Get the Latest News and Financial Analytics")
col2.write("ourhgeourhgeourgheourghoeurghwourghwourghwourghowu")

# for idx, page in enumerate(pages):
#     with tabs[idx]:
#         name = page.split("_")[0].capitalize()
#         st.markdown(f'<a href="{page}" target="_self">{name}</a>', unsafe_allow_html=True)

st.caption('Created by Torger Bocianowski')

