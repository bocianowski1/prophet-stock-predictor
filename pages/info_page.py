import streamlit as st
import yfinance as yf

def info_page():
    st.title('Additional Info🤔')
    # stock = st.text_input('Ticker', key='info field')
    stock = 'MSFT' 
    ticker = yf.Ticker(stock)

    # for i, action in enumerate(tabs_list):
    #     with tabs[i]:
    #         st.subheader(action)
    #         st.write(ticker.get_balance_sheet())


    # if len(stock) > 0:
        
    actions = {
        'Balance Sheet': ticker.get_balance_sheet(),
        'Earnings': ticker.get_earnings_history(),
        'Cash Flow': ticker.get_cashflow()
    }
    
    action = st.selectbox('Get insight', actions.keys(), key='action select')
    with st.spinner(f'Getting {action} for {stock.upper()}...'):
        st.subheader(f'{action} for {stock.upper()}')
        st.write(actions[f'{action}'])
    
