import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statsmodels.tsa.arima.model import ARIMA

# Load the data into a DataFrame
df = pd.read_csv(r"C:\Users\manas\Documents\IE0005_Project\Cities\bangalore.csv")  

# Combine 'date' and 'time' columns into a single datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'].astype(str).str.zfill(2) + ':00')

# Drop the original 'date' and 'time' columns
df.drop(['date', 'time'], axis=1, inplace=True)

# Set 'datetime' as the index
df.set_index('datetime', inplace=True)

WindowSize = 8

# Define function to train ARIMA model
def TrainCityARIMA(df, endog_column):
    # Select the endogenous variable (single column) from the DataFrame
    endog_data = df[endog_column]

    # Splitting data into training and testing sets
    train_data = endog_data.iloc[:-WindowSize]
    test_data = endog_data.iloc[-WindowSize:]

    arima_model = ARIMA(train_data, order=(5,1,0)) 
    arima_fit = arima_model.fit()

    predictions = arima_fit.forecast(steps=len(test_data))
    mse = np.mean((test_data.values - predictions)**2)
    print(f"Mean Squared Error: {mse}")

    plt.plot(test_data.index, predictions, color='red', label='Predictions')
    plt.plot(test_data.index, test_data.values, color='blue', label='Actual')
    plt.legend()
    plt.show()

endog_column = 'windspeed'

TrainCityARIMA(df, endog_column)
