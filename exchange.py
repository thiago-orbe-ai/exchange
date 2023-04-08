import streamlit as st
import pandas as pd
import numpy as np

# Define the currency pairs
currency_pairs = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'AUD/USD', 'NZD/USD']

# Define the currency index
currency_index = {
    'EUR/USD': 0,
    'USD/JPY': 1,
    'GBP/USD': 2,
    'USD/CHF': 3,
    'USD/CAD': 4,
    'AUD/USD': 5,
    'NZD/USD': 6
}

# Define the currency exchange rates
exchange_rates = np.array([
    [1.0, 1.2, 0.9, 1.1, 1.3, 0.8, 0.7],
    [0.8, 1.0, 0.7, 0.9, 1.1, 0.6, 0.5],
    [1.1, 1.4, 1.0, 1.2, 1.5, 0.9, 0.8],
    [0.9, 1.1, 0.8, 1.0, 1.2, 0.7, 0.6],
    [0.7, 0.9, 0.6, 0.8, 1.0, 0.5, 0.4],
    [1.2, 1.5, 1.1, 1.3, 1.6, 1.0, 0.9],
    [1.3, 1.6, 1.2, 1.4, 1.7, 1.1, 1.0]
])

# Define the function to compute the shortest distances and best routes using the Bellman-Ford algorithm
def bellman_ford(distances, source):
    n = len(distances)
    best_routes = [None] * n
    best_distances = [float('inf')] * n
    best_distances[source] = 0
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if distances[u][v] + best_distances[u] < best_distances[v]:
                    best_distances[v] = distances[u][v] + best_distances[u]
                    best_routes[v] = u
    return best_distances, best_routes

# Compute the distances between currency pairs
distances = np.zeros((len(currency_pairs), len(currency_pairs)))
for i in range(len(currency_pairs)):
    for j in range(len(currency_pairs)):
        distances[i][j] = -np.log(exchange_rates[i][j])

# Convert the distances matrix to a Pandas DataFrame
chart_data = pd.DataFrame(data=distances, columns=currency_pairs, index=currency_pairs)

# Add a new column to the chart_data DataFrame with the cumulative distances of the best route
best_distances, best_routes = bellman_ford(distances, 0)
chart_data['cumulative_distance'] = np.zeros(len(currency_pairs))
for i in range(len(currency_pairs)):
    if best_routes[i] is not None:
        chart_data.loc[currency_pairs[i], 'cumulative_distance'] = -best_distances[i]

# Display the chart
#Display the chart
st.line_chart(chart_data['cumulative_distance'], use_container_width=True)

#Trace the best route
st.write("Best route:")
for i in range(len(best_routes)):
    if best_routes[i] is not None:
        st.write(currency_pairs[i], "->", currency_pairs[best_routes[i]], "(Distance =", -best_distances[i], ")")

#Trace the complete route for the best scenario
if best_routes[-1] is not None:
    complete_route = [currency_pairs[-1]]
    current_currency = currency_pairs[-1]
    while current_currency != currency_pairs[0]:
        current_currency = currency_pairs[best_routes[currency_index[current_currency]]]
        complete_route.insert(0, current_currency)
        st.write("Complete route:", "->".join(complete_route))
else:
    st.write("No route found")
