import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from pypfopt import expected_returns, risk_models, EfficientFrontier
from deap import algorithms, base, creator, tools

# Define the Streamlit app
st.title("Stock Portfolio Optimizer with Genetic Algorithms")

# Define a function to retrieve the historical price data for a given stock symbol
def get_historical_price(symbol):
    stock_data = yf.download(symbol)
    return stock_data

# Define a function to calculate the fitness of a portfolio
def calculate_fitness(weights, returns, cov_matrix, target_return):
    portfolio_return = np.dot(returns, weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    penalty = np.abs(portfolio_return - target_return)
    return (1 / portfolio_volatility) - penalty

# Add a text input for the list of stock symbols
symbol_list = st.text_input("Enter a comma-separated list of stock symbols (e.g. AAPL,MSFT,AMZN)")

# Add a slider for the target return
target_return = st.slider("Target Return", min_value=0.0, max_value=1.0, value=0.1, step=0.01)

if symbol_list:
    # Split the input string into a list of stock symbols
    symbol_list = symbol_list.split(",")
    symbol_list = [symbol.strip().upper() for symbol in symbol_list]

    # Retrieve the historical price data for each stock symbol
    stock_data = pd.DataFrame()
    for symbol in symbol_list:
        data = get_historical_price(symbol)
        data = pd.DataFrame(data['Adj Close'])
        data.columns = [symbol]
        stock_data = pd.concat([stock_data, data], axis=1)

    # Calculate the expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(stock_data)
    S = risk_models.sample_cov(stock_data)

    # Define the fitness function
    def fitness_function(weights):
        return calculate_fitness(weights, mu, S, target_return)

    # Define the genetic algorithm
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("attr_weight", np.random.uniform, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_weight, len(symbol_list))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", fitness_function)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)
    population = toolbox.population(n=100)
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    best_individual = tools.selBest(offspring, k=1)[0]

    # Display the optimal portfolio weights and expected returns
    st.write(f"Optimal Portfolio Weights: {best_individual}")
    st.write(f"Expected Returns: {calculate_fitness(best_individual, mu, S
