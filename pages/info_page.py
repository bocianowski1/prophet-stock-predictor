import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from plotly import graph_objs
import plotly.express as px

def info_page(tickers):
    st.title('Additional Info')
    tabs_list = [
        'Balance Sheet',
        'Cash Flow',
        'Earnings',
    ]
    try:
        stock = st.selectbox('Select a company', tickers, key='info select')
        ticker = yf.Ticker(stock)
        tabs = st.tabs(tabs_list)
    
        with tabs[0]:
            st.subheader('Balance Sheet')
            df = ticker.balance_sheet
            df.columns = [date.strftime("%d/%m/%Y") for date in df.columns]
            # df = df.floordiv(1_000_000_000)
            df = df.fillna(0)
            st.dataframe(df, use_container_width=True)

        with tabs[1]:
            st.subheader('Cash Flow')
            df = ticker.cashflow
            df.columns = [date.strftime("%d/%m/%Y") for date in df.columns]
            df = df.fillna(0)
            st.dataframe(df, use_container_width=True)

            with st.expander('Cash Flow Bar Chart'):
                year = st.selectbox('Year to display', df.columns)
                st.bar_chart(df[year])

    
        with tabs[2]:
            st.subheader('Earnings')
            df = ticker.earnings
            df = df.fillna(0)
            col1, col2 = st.columns(2)
            col1.dataframe(df, use_container_width=True)
            col2.bar_chart(df)
    
    
    
        infos = [
                'ebitda', 'grossProfits', 'freeCashflow', 'operatingCashflow', 
                'currentRatio', 'targetMeanPrice', 'debtToEquity', 'totalCash'
                ]

        vals = [ticker.info[info] for info in infos]
        vals = np.array([vals, np.ones(len(vals))])

        info_df = pd.DataFrame(
                vals, columns=infos
            )

        st.subheader(f'More Info about {stock}')
        col1, col2 = st.columns(2)
        col1.table(
            info_df[:1].T
            .iloc[: int(len(info_df.T)/2)]
        )
        col2.table(
            info_df[:1].T
            .iloc[int(len(info_df.T)/2):]
        )
        st.subheader(f'\nAbout {stock}')
        st.write(ticker.info['longBusinessSummary'])

    except:
        st.text(f'There was an issue loading the data for {stock}')
    # st.text('Response')
    # st.write(ticker.info)
        
    
    
