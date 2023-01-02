import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# def info_page(tickers: pd.DataFrame):
tickers = pd.read_csv('data/marketcap.csv')
st.title('Additional Info')
tabs_list = [
    'Balance Sheet',
    'Cash Flow',
    'Earnings',
]
try:
    stock = st.selectbox('Select a company', tickers['Ticker'], key='info select')
    ticker = yf.Ticker(stock)
    tabs = st.tabs(tabs_list)

    with tabs[0]:
        st.subheader('Balance Sheet')
        df = ticker.balance_sheet
        df.columns = [date.strftime("%d/%m/%Y") for date in df.columns]
        df = df.fillna(0)
        styled = df.style.format("{:,}")
        st.dataframe(styled, use_container_width=True)

    with tabs[1]:
        st.subheader('Cash Flow')
        df = ticker.cashflow
        df.columns = [date.strftime("%d/%m/%Y") for date in df.columns]
        df = df.fillna(0)
        styled = df.style.format("{:,}")
        st.dataframe(styled, use_container_width=True)

    with tabs[2]:
        st.subheader('Earnings')
        df = ticker.earnings
        df = df.fillna(0)
        styled = df.style.format("{:,}")
        col1, col2 = st.columns(2)
        col1.dataframe(styled, use_container_width=True)
        col2.bar_chart(df, use_container_width=True)
        # reset = df.reset_index()
        # print(reset)
        # print(reset['Year'])
        # fig = plt.figure(figsize=(8, 6))
        # sns.barplot(data=reset, x='Revenue', y='Earnings', hue='Year')
        # col2.pyplot(fig)

    infos = [
            'ebitda', 'grossProfits', 'freeCashflow', 'operatingCashflow', 
            'totalCash', 'currentRatio', 'targetMeanPrice', 'debtToEquity'
            ]

    vals = [ticker.info[info] for info in infos]
    vals = np.array([vals, np.ones(len(vals))])

    info_df = pd.DataFrame(vals, columns=infos)

    st.subheader(f'More Info about {stock}')
    col1, col2 = st.columns(2)
    col1.table(
        info_df[:1].T
        .iloc[: int(len(info_df.T)/2)].style.format("{:,}")
    )
    col2.table(
        info_df[:1].T
        .iloc[int(len(info_df.T)/2):].style.format("{:,}")
    )
    st.subheader(f'\nAbout {stock}')
    st.write(ticker.info['longBusinessSummary'])

except:
    st.text(f'There was an issue loading the data for {stock}')


