import streamlit as st
import numpy as np

def bellman_ford(adj_matrix, source):
    n = len(adj_matrix)
    distances = [np.inf for i in range(n)]
    distances[source] = 0
    best_routes = [None for i in range(n)]

    for k in range(n-1):
        for i in range(n):
            for j in range(n):
                if adj_matrix[i][j] != 0:
                    if distances[i] + adj_matrix[i][j] < distances[j]:
                        distances[j] = distances[i] + adj_matrix[i][j]
                        best_routes[j] = i

    return distances, best_routes

# Define the distances between major currency pairs
distances = [
    [0, 0.8, 1.3, 1.0, 1.2, 1.5, 1.9],
    [0.8, 0, 1.1, 0.9, 0.9, 1.2, 1.6],
    [1.3, 1.1, 0, 1.7, 1.6, 1.8, 2.1],
    [1.0, 0.9, 1.7, 0, 0.8, 1.1, 1.5],
    [1.2, 0.9, 1.6, 0.8, 0, 1.3, 1.7],
    [1.5, 1.2, 1.8, 1.1, 1.3, 0, 0.4],
    [1.9, 1.6, 2.1, 1.5, 1.7, 0.4, 0]
]

# Define the major currency pairs
currency_pairs = ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'AUD/USD', 'NZD/USD']

# Define a dictionary to map currency pairs to their indices in the distance matrix
currency_index = {currency_pairs[i]: i for i in range(len(currency_pairs))}

    # Create a dropdown to select the source currency pair
    source_currency = st.selectbox("Select the source currency pair", currency_pairs)

    # Get the index of the source currency pair
    source_index = currency_index[source_currency]

    # Calculate the shortest distances and best routes
    distances, best_routes = bellman_ford(distances, source_index)

    # Display the results
    st.write("Distance from", source_currency)
    for i in range(len(currency_pairs)):
        if i != source_index:
            st.write(source_currency, "to", currency_pairs[i], "=", distances[i])

    # Highlight the best route in the chart
    best_routes = [best_routes[i] for i in range(len(best_routes))]

    # Create a dictionary to map currency pairs to their colors in the chart
    color_map = {
        'EUR/USD': 'blue',
        'USD/JPY': 'orange',
        'GBP/USD': 'green',
        'USD/CHF': 'red',
        'USD/CAD': 'purple',
        'AUD/USD': 'brown',
        'NZD/USD': 'pink'
    }

    # Display the chart
    st.line_chart(chart_data, use_container_width=True)

    # Trace the best route
    st.write("Best route:")
    for i in range(len(best_routes)):
        if best_routes[i] is not None:
            st.write(currency_pairs[i], "->", currency_pairs[best_routes[i]], "(Distance =", distances[best_routes[i]], ")")
