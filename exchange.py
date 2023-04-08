import streamlit as st
import pandas as pd
import numpy as np

# Define the Bellman-Ford algorithm function
def bellman_ford(source, currency_pairs, exchange_rates):
    num_currencies = len(currency_pairs)
    distances = [np.inf] * num_currencies
    best_routes = [None] * num_currencies
    distances[source] = 0
    
    for i in range(num_currencies - 1):
        for j in range(num_currencies):
            for k in range(num_currencies):
                if exchange_rates[j][k] != np.inf and distances[j] + np.log(exchange_rates[j][k]) < distances[k]:
                    distances[k] = distances[j] + np.log(exchange_rates[j][k])
                    best_routes[k] = j
                    
    # Check for negative cycles
    for j in range(num_currencies):
        for k in range(num_currencies):
            if exchange_rates[j][k] != np.inf and distances[j] + np.log(exchange_rates[j][k]) < distances[k]:
                return None, None, None
    
    # Convert distances to negative log-likelihoods
    for i in range(num_currencies):
        distances[i] = -distances[i]
    
    return distances, best_routes, currency_pairs

# Define the currency pairs and exchange rates
currency_pairs = ["USD/EUR", "EUR/JPY", "JPY/USD", "USD/GBP", "GBP/EUR", "EUR/CHF", "CHF/JPY"]
exchange_rates = np.array([
    [np.inf, 0.84, np.inf, 0.72, np.inf, np.inf, np.inf],
    [1.19, np.inf, 109.91, np.inf, 0.85, np.inf, 130.45],
    [np.inf, 0.0091, np.inf, np.inf, np.inf, np.inf, 0.0076],
    [1.38, np.inf, np.inf, np.inf, 0.71, np.inf, np.inf],
    [np.inf, 1.18, np.inf, 1.41, np.inf, 1.13, np.inf],
    [1.09, np.inf, np.inf, np.inf, 0.88, np.inf, 117.74],
    [np.inf, 0.0077, 130.83, np.inf, np.inf, 0.0085, np.inf]
])

# Create the user interface
st.title("Forex Arbitrage Finder")

# Display the currency pairs and exchange rates
st.write("Currency pairs:")
st.write(pd.DataFrame(exchange_rates, index=currency_pairs, columns=currency_pairs))

# Select the source currency
source_currency = st.selectbox("Select the source currency:", currency_pairs)

# Run the Bellman-Ford algorithm
distances, best_routes, currency_pairs = bellman_ford(currency_pairs.index(source_currency), currency_pairs, exchange_rates)

# Display the results
if distances is None:
    st.write("Negative cycle detected")
else:
    # Create a dataframe to display the distances and best routes
    data = {"Distance": distances, "Best Route": best_routes}
    df = pd.DataFrame(data, index=currency_pairs)
    st.write("Distances and Best Routes:")
    st.write(df)
    
    # Create a chart to show the best route
    chart_data = pd.DataFrame({"distance": distances, "currency_pair": currency_pairs})
    chart_data = chart_data.sort_values(by="distance", ascending=False)
    st.line_chart(chart_data, use_container_width=True)

    # Trace the best route
    st.write("Best route:")
    for i in range(len(best_routes)):
        if best_routes[i] is not None:
            st.write(currency_pairs[i], "->", currency_pairs[best_routes[i]], "(Distance =", distances[best_routes[i]], ")")
