import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

def get_exchange_rate(from_currency, to_currency):
    ticker = f"{from_currency}{to_currency}=X"
    data = yf.download(tickers=ticker, period="1d", interval="1m")
    return data["Close"].iloc[-1]

def bellman_ford(currencies, initial_amount=1):
    n = len(currencies)
    distances = [float("inf")] * n
    amounts = [0] * n
    amounts[0] = initial_amount
    distances[0] = 0
    for i in range(n - 1):
        for j in range(n):
            for k in range(n):
                if j != k:
                    exchange_rate = get_exchange_rate(currencies[j], currencies[k])
                    if distances[k] > distances[j] + exchange_rate:
                        distances[k] = distances[j] + exchange_rate
                        amounts[k] = amounts[j] * (1 / exchange_rate)
    for j in range(n):
        for k in range(n):
            if j != k:
                exchange_rate = get_exchange_rate(currencies[j], currencies[k])
                if distances[k] == distances[j] + exchange_rate:
                    if amounts[k] < amounts[j] * (1 / exchange_rate):
                        amounts[k] = amounts[j] * (1 / exchange_rate)
    return distances, amounts

currencies = st.text_input("Enter currencies separated by commas (e.g. USD,EUR,GBP)").upper().split(",")
initial_amount = st.number_input("Enter initial amount", min_value=0.01, value=100.0, step=0.01, format="%.2f")
if len(currencies) > 1:
    distances, amounts = bellman_ford(currencies, initial_amount)
    st.write(f"The best route is {currencies[0]} -> {currencies[-1]}")
    st.write(f"The total exchange rate is {distances[-1]:.6f}")
    for i in range(len(currencies) - 1):
        st.write(f"- Buy {amounts[i]:.2f} {currencies[i]}")
        if i < len(currencies) - 1:
            st.write(f"- Sell {amounts[i + 1]:.2f} {currencies[i + 1]}")
else:
    st.write("Please enter at least 2 currencies.")
