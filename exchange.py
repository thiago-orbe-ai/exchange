import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yf

# Define the app layout
st.title("Forex Route Optimizer")
st.write("Enter the currencies and amount to exchange")

currency_list = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW', 'SGD', 'NOK', 'MXN', 'INR']
currency_from = st.selectbox("From", currency_list)
currency_to = st.selectbox("To", currency_list)
amount = st.number_input("Amount to exchange", min_value=1)

# Get forex data
start_date = pd.to_datetime('2020-01-01')
end_date = pd.to_datetime(pd.Timestamp.today().date())

forex_data = pdr.get_data_yahoo(f"{currency_from}{currency_to}=X", start_date, end_date)

# Calculate the best forex route
routes = [['USD', 'EUR', 'JPY', 'USD'], ['USD', 'EUR', 'JPY', 'EUR', 'USD'], ['USD', 'EUR', 'JPY', 'EUR', 'JPY', 'USD'], ['USD', 'EUR', 'JPY', 'EUR', 'JPY', 'EUR', 'USD']]
best_route = None
best_rate = None
for route in routes:
    rate = 1
    for i in range(len(route)-1):
        pair = f"{route[i]}{route[i+1]}=X"
        rate *= pdr.get_data_yahoo(pair, start_date, end_date)['Close'].iloc[-1]
    if not best_rate or rate > best_rate:
        best_rate = rate
        best_route = route

# Display the results
st.write(f"The best route to exchange {currency_from} to {currency_to} is {' -> '.join(best_route)}")
st.write(f"The exchange rate is {round(best_rate, 4)}")
st.write(f"The amount received is {round(best_rate * amount, 2)} {currency_to}")
