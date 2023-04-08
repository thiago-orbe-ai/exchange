import numpy as np
import streamlit as st

# Define the forex graph
forex_graph = np.array([
    [0.0, 1.25, 0.9, 0.8],
    [0.8, 0.0, 0.6, 0.7],
    [1.1, 1.67, 0.0, 1.2],
    [1.25, 1.43, 0.83, 0.0]
])

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
st.title('Forex Bellman-Ford')

# Get the source currency pair from the user
source = st.selectbox('Select the source currency pair:', ['USD/EUR', 'USD/GBP', 'USD/JPY', 'EUR/GBP'])

# Map the currency pair to an index in the forex graph
source_map = {'USD/EUR': 0, 'USD/GBP': 1, 'USD/JPY': 2, 'EUR/GBP': 3}
source_index = source_map[source]

# Compute the shortest distances using Bellman-Ford
distances = bellman_ford(forex_graph, source_index)

# Display the
