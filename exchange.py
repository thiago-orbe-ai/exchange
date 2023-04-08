import streamlit as st
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf

# Calculate the best forex route
def calculate_rate(route):
    rate = 1
    for i in range(len(route)-1):
        pair = f"{route[i]}{route[i+1]}=X"
        rate *= forex_data[pair]['Close'].iloc[-1]
    return rate

# Define the app layout
st.title("Forex Route Optimizer")
st.write("Enter the currencies and amount to exchange")

currency_list = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'HKD', 'NZD', 'SEK', 'KRW', 'SGD', 'NOK', 'MXN', 'INR']
currency_from = st.selectbox("From", currency_list)
currency_to = st.selectbox("To", currency_list)
amount = st.number_input("Amount to exchange", min_value=1)

if st.button("Run"):
          # Get forex data
          start_date = pd.to_datetime('2020-01-01')
          end_date = pd.to_datetime(pd.Timestamp.today().date())

          forex_data = {}
          for i in range(len(currency_list)):
              for j in range(i+1, len(currency_list)):
                  pair = f"{currency_list[i]}{currency_list[j]}=X"
                  forex_data[pair] = pdr.get_data_yahoo(pair, start_date, end_date)

          routes = [[currency_from, currency_to]]
          for i in range(len(currency_list)):
              for j in range(i+1, len(currency_list)):
                  if currency_list[i] == currency_from and currency_list[j] == currency_to:
                      continue
                  route1 = [currency_from, currency_list[i], currency_list[j], currency_to]
                  rate1 = calculate_rate(route1)
                  route2 = [currency_from, currency_list[j], currency_list[i], currency_to]
                  rate2 = calculate_rate(route2)
                  if rate1 > rate2:
                      route1.reverse()
                      rate1 = 1 / rate1
                  routes.append(route1)

          transaction_cost = 0.0001
          best_route = None
          best_rate = None
          for route in routes:
              rate = calculate_rate(route)
              cost = 1
              for i in range(len(route)-1):
                  pair = f"{route[i]}{route[i+1]}=X"
                  cost *= (1 + transaction_cost) / (1 - transaction_cost * forex_data[pair]['Close'].iloc[-1])
              total_cost = (cost - 1) * amount
              total_amount = amount * rate * (1 - total_cost)
              if not best_rate or total_amount > best_rate * (1 - total_cost):
                  best_rate = total_amount / amount
                  best_route = route

          # Display the results
          st.write(f"The best route to exchange {currency_from} to {currency_to} is {' -> '.join(best_route)}")
          st.write(f"The exchange rate is {round(best_rate, 4)}")
          st.write(f"The amount received is {round(best_rate * amount * (1 - total_cost), 2)} {currency_to}")
          st.write(f"The total cost is {round(total_cost * amount, 2)} {currency_from}")
