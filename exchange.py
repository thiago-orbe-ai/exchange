import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.write('## Forex Route of Exchanges')
st.write('### Data')
st.write('Exchange rates will be fetched from Yahoo Finance using the yfinance library.')

st.write('## Forex Route of Exchanges')
st.write('### Data')
st.write('Exchange rates will be fetched from Yahoo Finance using the yfinance library.')

st.write('### User Inputs')
from_currency = st.selectbox('Select the currency you want to convert from:', ['USD', 'EUR', 'GBP', 'JPY'])
to_currency = st.selectbox('Select the currency you want to convert to:', ['USD', 'EUR', 'GBP', 'JPY'])
amount = st.number_input('Enter the amount you want to convert:', min_value=0.0, max_value=1000000.0, value=1000.0, step=100.0)

st.write('### User Inputs')
from_currency = st.selectbox('Select the currency you want to convert from:', ['USD', 'EUR', 'GBP', 'JPY'])
to_currency = st.selectbox('Select the currency you want to convert to:', ['USD', 'EUR', 'GBP', 'JPY'])
amount = st.number_input('Enter the amount you want to convert:', min_value=0.0, max_value=1000000.0, value=1000.0, step=100.0)

# Define function to get exchange rate from yfinance
def get_exchange_rate(from_currency, to_currency):
    ticker = f'{from_currency}{to_currency}=X'
    exchange_rate = yf.Ticker(ticker).history(period='1d')['Close'][0]
    return exchange_rate

# Get the available exchange rates for the selected currencies
available_rates = []
for currency in [from_currency, to_currency]:
    if currency != 'USD':
        usd_rate = get_exchange_rate(currency, 'USD')
        available_rates.append(usd_rate)
if len(available_rates) == 1:
    from_currency = 'USD' if from_currency != 'USD' else to_currency
    to_currency = 'USD' if to_currency != 'USD' else from_currency
    usd_rate = get_exchange_rate(from_currency, to_currency)
    available_rates = [usd_rate]
else:
    for currency in ['USD', from_currency, to_currency]:
        if currency not in [from_currency, to_currency]:
            usd_rate = get_exchange_rate(currency, 'USD')
            available_rates.append(usd_rate)

# Calculate the amount of money after each exchange
amounts_after_exchange = [amount]
for rate in available_rates:
    amount_after_exchange = amounts_after_exchange[-1] * rate
    amounts_after_exchange.append(amount_after_exchange)

# Calculate the percentage change in amount after each exchange
percent_changes = []
for i in range(len(amounts_after_exchange)-1):
    percent_change = (amounts_after_exchange[i+1] - amounts_after_exchange[i]) / amounts_after_exchange[i] * 100
    percent_changes.append(percent_change)

# Find the index of the maximum percentage change
max_index = np.argmax(percent_changes)

# Print the optimal forex route
st.write('### Output')
st.write('Optimal Forex Route:')
for i in range(len(available_rates)):
    rate = available_rates[i]
    if i == max_index:
        st.write(f'{from_currency} -> {to_currency} ({rate:.4f}) (Optimal)')
    else:
        st.write(f'{from_currency} -> USD ({rate:.4f}) -> {to
