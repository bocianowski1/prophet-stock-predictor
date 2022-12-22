import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

def info_page(tickers):
    st.title('Additional Info')
    tabs_list = [
        'Balance Sheet',
        'Cash Flow',
        'Earnings',
    ]
    stock = st.selectbox('Select a company', tickers, key='info select')
    ticker = yf.Ticker(stock)
    tabs = st.tabs(tabs_list)

        
    actions = {
        'Balance Sheet': ticker.balance_sheet,
        'Cash Flow': ticker.cashflow,
        'Earnings': ticker.earnings,
    }

    for i, action in enumerate(actions):
        with tabs[i]:
            with st.spinner(f'Getting {action} for {stock.upper()}...'):
                st.subheader(action)
                df = actions[action]
                if type(df.columns[0]) == pd._libs.tslibs.timestamps.Timestamp:
                    cols = [date.strftime("%d/%m/%Y") for date in df.columns]
                    df.columns = cols
                st.write(df)
    
    
    infos = [
            'ebitda', 'grossProfits', 'freeCashflow', 'operatingCashflow', 
            'currentRatio', 'targetMeanPrice', 'debtToEquity', 'totalCash'
            ]

    vals = [ticker.info[info] for info in infos]
    vals = np.array([vals, np.ones(len(vals))])

    info_df = pd.DataFrame(
            vals, columns=infos
        )

    st.subheader(f'More Info about {stock.upper()}')
    col1, col2 = st.columns(2)
    col1.table(
        info_df[:1].T
        .iloc[: int(len(info_df.T)/2)]
    )
    col2.table(
        info_df[:1].T
        .iloc[int(len(info_df.T)/2):]
    )
    st.subheader(f'\nAbout {stock.upper()}')
    st.write(ticker.info['longBusinessSummary'])

    st.text('Response')
    st.write(ticker)
        
    
    
