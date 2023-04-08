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
    # Initialize the distances and best routes to infinity and None respectively
    distances = np.full(len(forex_graph), np.inf)
    best_routes = [None] * len(forex_graph)
    
    # Set the distance to the source to zero
    distances[source] = 0.0
    
    # Iterate over all edges n - 1 times
    for i in range(len(forex_graph) - 1):
        # Iterate over all edges
        for j in range(len(forex_graph)):
            for k in range(len(forex_graph)):
                if forex_graph[j][k] != 0.0 and distances[j] + forex_graph[j][k] < distances[k]:
                    distances[k] = distances[j] + forex_graph[j][k]
                    best_routes[k] = j

    return distances, best_routes

# Define the Streamlit app
st.title('Forex Bellman-Ford')

# Get the source currency pair from the user
source = st.selectbox('Select the source currency pair:', ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'AUD/USD', 'NZD/USD'])

# Map the currency pair to an index in the forex graph
source_map = {'EUR/USD': 0, 'USD/JPY': 1, 'GBP/USD': 2, 'USD/CHF': 3, 'USD/CAD': 4, 'AUD/USD': 5, 'NZD/USD': 6}
source_index = source_map[source]

# Compute the shortest distances and best routes using Bellman-Ford
distances, best_routes = bellman_ford(forex_graph, source_index)

# Display the best route as a chart
chart_data = {
    'source: [source],
'destination': ['EUR/USD', 'USD/JPY', 'GBP/USD', 'USD/CHF', 'USD/CAD', 'AUD/USD', 'NZD/USD'],
'distance': distances,
'best_route': best_routes
}
st.write(chart_data)

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

# Create a list of colors for the edges in the chart
edge_colors = [color_map[chart_data['destination'][i]] for i in range(len(chart_data['destination']))]

# Create a list of edge labels for the chart
edge_labels = [f"Best route: {chart_data['source'][best_routes[i]]} -> {chart_data['destination'][i]}" if best_routes[i] is not None else "" for i in range(len(best_routes))]

# Create the chart
st.graphviz_chart(f"""
digraph {{
    node [style=filled]
    {source} [color=black, fillcolor=gray]
    {"; ".join(chart_data['destination'])}
    {"; ".join([f"{chart_data['source'][i]} -> {chart_data['destination'][i]} [label={chart_data['distance'][i]}]" for i in range(len(chart_data['destination']))])}
    {"; ".join([f"{chart_data['source'][best_routes[i]]} -> {chart_data['destination'][i]} [color={color_map[chart_data['destination'][i]]}, label=\"{edge_labels[i]}\"]" for i in range(len(best_routes)) if best_routes[i] is not None])}
}}
""", engine='dot', format='svg', edge_attributes={'color': edge_colors})

