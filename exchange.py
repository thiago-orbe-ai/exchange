import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

def get_exchange_rate(from_currency, to_currency):
    ticker = f"{from_currency}{to_currency}=X"
    data = yf.download(tickers=ticker, period="1d", interval="1m")
    return data["Close"].iloc[-1]

def bellman_ford(currencies):
    n = len(currencies)
    distances = [float("inf")] * n
    distances[0] = 0
    for i in range(n - 1):
        for j in range(n):
            for k in range(n):
                if j != k:
                    exchange_rate = get_exchange_rate(currencies[j], currencies[k])
                    if distances[k] > distances[j] + exchange_rate:
                        distances[k] = distances[j] + exchange_rate
    return distances

tickers = yf.Tickers("aapl")  # We just need a Tickers object to access the yfinance currency list
info = tickers.tickers["aapl"].info

currency_set = set()
for ticker, data in info.items():
    if "currency" in data:
        currency_set.add(data["currency"])
currency_list = sorted(list(currency_set))
currencies = options = st.multiselect(currency_list)

if st.button("Run"):
    if len(currencies) > 1:
        distances = bellman_ford(currencies)
        st.write(f"The best route is {currencies[0]} -> {currencies[-1]}")
        st.write(f"The total exchange rate is {distances[-1]}")
    else:
        st.write("Please enter at least two currencies.")
