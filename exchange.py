import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Create a function to solve the Bellman-Ford problem
def bellman_ford(currency_pairs, exchange_rates, start_currency):
    n_currencies = len(currency_pairs)
    distances = [float("inf") for i in range(n_currencies)]
    distances[start_currency] = 0
    best_routes = [None for i in range(n_currencies)]
    for i in range(n_currencies - 1):
        for j in range(n_currencies):
            for k in range(n_currencies):
                if distances[k] + exchange_rates[k][j] < distances[j]:
                    distances[j] = distances[k] + exchange_rates[k][j]
                    best_routes[j] = k
    # Check for negative cycles
    for j in range(n_currencies):
        for k in range(n_currencies):
            if distances[k] + exchange_rates[k][j] < distances[j]:
                st.error("Error: Negative cycle detected")
                return None, None
    return distances, best_routes

# Define the currency pairs and exchange rates
currency_pairs = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF"]
exchange_rates = [
    [1.0, 0.818, 0.707, 1.251, 1.320, 109.680, 0.897],
    [1.223, 1.0, 0.862, 1.530, 1.614, 132.730, 1.088],
    [1.414, 1.159, 1.0, 1.772, 1.868, 153.280, 1.254],
    [0.800, 0.656, 0.565, 1.0, 1.053, 86.370, 0.709],
    [0.758, 0.620, 0.534, 0.949, 1.0, 82.160, 0.673],
    [0.009, 0.008, 0.007, 0.012, 0.012, 1.0, 0.008],
    [1.116, 0.918, 0.791, 1.402, 1.477, 121.200, 1.0]
]

# Define the start currency
start_currency = 0

# Solve the Bellman-Ford problem
distances, best_routes = bellman_ford(currency_pairs, exchange_rates, start_currency)

# Display the distances
st.write("Distances from", currency_pairs[start_currency])
chart_data = pd.DataFrame(distances, columns=["Distance"], index=currency_pairs)
st.write(chart_data)

# Display the chart
st.line_chart(chart_data['Distance'], use_container_width=True)

# Trace the best route
st.write("Best route:")
for i in range(len(best_routes)):
    if best_routes[i] is not None:
        st.write(currency_pairs[i], "->", currency_pairs[best_routes[i]], "(Distance =", distances[best_routes[i]], ")")

# Optimize the best route
optimized_route = [currency_pairs[start_currency]]
while best_routes[start_currency] is not None:
    optimized_route.append(currency_pairs[best_routes[start_currency]])
    start_currency = best_routes[start_currency]
st.write("Optimized route:", " -> ".join(optimized_route))

# Create a graph of the currency pairs

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import bellman_ford

# Define the currency pairs and their exchange rates
currency_pairs = ["USDJPY", "EURUSD", "GBPUSD", "USDCHF", "AUDUSD"]
exchange_rates = np.array([
    [1, 110.197, 0.778497, 0.924166, 0.759464],
    [0.00906507, 1, 1.41624, 1.68222, 1.37823],
    [1.28369, 0.705909, 1, 1.18726, 0.972304],
    [1.08126, 0.594184, 0.841228, 1, 0.819142],
    [1.31661, 0.725609, 1.02822, 1.22098, 1]])

# Convert exchange rates to distances
distances = -np.log(exchange_rates)

# Create a matrix with the distances between each currency pair
matrix = csr_matrix(distances)

# Calculate the shortest distance between each currency pair using the Bellman-Ford algorithm
dist, pred = bellman_ford(matrix, return_predecessors=True)

# Find the best route to convert a currency to another
best_routes = []
for i in range(len(currency_pairs)):
    route = None
    for j in range(len(currency_pairs)):
        if i != j:
            intermediate_currency = pred[i, j]
            if intermediate_currency != -9999:
                if route is None or dist[i, intermediate_currency] + dist[intermediate_currency, j] < dist[route[0], route[1]]:
                    route = (i, intermediate_currency, j)
    best_routes.append(route[1] if route is not None else None)

# Display the chart
chart_data = {'distance': distances[best_routes]}
st.line_chart(chart_data, use_container_width=True)

# Trace the best route
st.write("Best route:")
for i in range(len(best_routes)):
    if best_routes[i] is not None:
        st.write(currency_pairs[i], "->", currency_pairs[best_routes[i]], "(Distance =", distances[i, best_routes[i]], ")")

# Optimize the best route
optimized_route = []
for i in range(len(best_routes)):
    if best_routes[i] is not None:
        route = [i, best_routes[i]]
        while True:
            intermediate_currency = pred[route[-2], route[-1]]
            if intermediate_currency != -9999:
                route.insert(-1, intermediate_currency)
            else:
                break
        optimized_route.extend(route[:-1])

# Display the optimized route
st.write("Optimized route:")
for i in range(len(optimized_route)-1):
    st.write(currency_pairs[optimized_route[i]], "->", currency_pairs[optimized_route[i+1]], "(Distance =", distances[optimized_route[i], optimized_route[i+1]], ")")
