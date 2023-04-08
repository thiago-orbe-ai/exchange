import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import yfinance as yf

def get_exchange_rates(currencies):
    # Create an empty DataFrame with currencies as columns and index
    df = pd.DataFrame(columns=currencies, index=currencies)
    
    # Fill the DataFrame with exchange rates
    for i in range(len(currencies)):
        for j in range(len(currencies)):
            if i == j:
                df.iloc[i,j] = 1.0
            else:
                pair = currencies[i] + currencies[j] + "=X"
                data = yf.download(pair, start="2021-01-01", end="2023-04-08")
                df.iloc[i,j] = data["Close"][-1]
                
    return df

def get_best_route(df, start_currency):
    # Create a graph from the DataFrame
    G = nx.from_pandas_adjacency(df)
    
    # Compute the shortest paths from the starting currency
    paths = nx.shortest_path(G, source=start_currency)
    
    # Compute the exchange rate for each path
    exchange_rates = []
    for currency, path in paths.items():
        exchange_rate = 1.0
        for i in range(len(path)-1):
            exchange_rate *= df.loc[path[i], path[i+1]]
        exchange_rates.append((currency, exchange_rate))
    
    # Sort the exchange rates and return the best route
    best_route = sorted(exchange_rates, key=lambda x: x[1])[0]
    
    return best_route

# Set the page title
st.set_page_config(page_title="Exchange Route", page_icon=":money_with_wings:")

# Define the app
# Set the app title
st.title("Exchange Route")

# Define the available currencies
currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY"]

# Get the exchange rates
exchange_rates = get_exchange_rates(currencies)

# Select the starting currency
start_currency = st.selectbox

# Select the starting currency
start_currency = st.selectbox("Select starting currency", currencies)
# Compute the best route
if st.button("Run"):
    best_route = get_best_route(exchange_rates, start_currency)
    # Display the best route
    st.write(f"The best exchange route starting from {start_currency} is:")
    st.write(best_route[0])
    st.write(f"Exchange rate: {best_route[1]:.4f}")

    # Plot the exchange rates as a heatmap
    fig, ax = plt.subplots()
    im = ax.imshow(exchange_rates.values.astype(float), cmap="coolwarm")
    ax.set_xticks(np.arange(len(currencies)))
    ax.set_yticks(np.arange(len(currencies)))
    ax.set_xticklabels(currencies)
    ax.set_yticklabels(currencies)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    ax.set_title("Exchange Rates")
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Exchange Rate", rotation=-90, va="bottom")
    st.pyplot(fig)

