# Import the required libraries
import numpy as np
import streamlit as st

# Define the forex graph
forex_graph = np.array([
    [0.0, 1.17, 1.38, 0.92, 0.78, 110.68, 0.92],
    [0.85, 0.0, 1.18, 0.79, 0.67, 95.50, 0.85],
    [0.72, 0.85, 0.0, 0.67, 0.57, 80.12, 0.67],
    [1.09, 1.29, 1.49, 0.0, 1.18, 132.17, 1.11],
    [1.28, 1.51, 1.75, 0.84, 0.0, 150.51, 0.84],
    [0.009, 0.010, 0.012, 0.005, 0.007, 0.0, 0.005],
    [1.09, 1.29, 1.49, 0.84, 1.18, 132.17, 0.0]
])

# Define the Bellman-Ford function
def bellman_ford(forex_graph, source):
    # Initialize the distances to infinity
    distances = np.full(len(forex_graph), np.inf)
    distances[source] = 0.0

    # Iterate over all edges n - 1 times
    for i in range(len(forex_graph) - 1):
        # Iterate over all edges
        for j in range(len(forex_graph)):
            for k in range(len(forex_graph)):
                if forex_graph[j][k] != 0.0 and distances[j] + forex_graph[j][k] < distances[k]:
                    distances[k] = distances[j] + forex_graph[j][k]

    return distances

# Define the Streamlit app
def app():
    st.title('Forex Bellman-Ford')
    
    # Get the source currency pair from the user
    source = st.selectbox('Select the source currency pair:', ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'AUD/USD', 'NZD/USD'])

    # Map the currency pair to an index in the forex graph
    source_map = {'EUR/USD': 0, 'USD/JPY': 1, 'GBP/USD': 2, 'USD/CHF': 3, 'USD/CAD': 4, 'AUD/USD': 5, 'NZD/USD': 6}
    source_index = source_map[source]

    # Compute the shortest distances using Bellman-Ford
    distances = bellman_ford(forex_graph, source_index)

    # Display the shortest distances
    for i, distance in enumerate(distances):
        if i != source_index:
            st.write(f"{source} to {'EUR/USD' if i == 0 else 'USD/JPY' if i == 1 else 'GBP/USD' if i == 2 else 'USD/CHF' if i == 3 else 'USD/CAD' if i == 4 else 'AUD/USD' if
