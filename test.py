import tensorflow as tf
import keras
import pandas as pd
import numpy as np
import os
from pathlib import Path

NumFeatures = 7
WindowSize = 8
cities = ["shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata"]

# Loading trained model checkpoints for each city
def LoadModel(city):
    model = keras.Sequential()
    model.add(tf.keras.layers.GRU(128, return_sequences=True))
    model.add(tf.keras.layers.GRU(128))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dense(7, activation='tanh'))
    model.build(input_shape=(None, WindowSize - 1, NumFeatures))

    checkpoint = tf.train.Checkpoint(model)
    directory = "C:/Users/manas/Documents/IE0005_Project/Checkpoints/"
    checkpoint.restore(directory + city + "Checkpoint").expect_partial()
    return model

# Loading additional test data for each city
def LoadTestData(city):
    test_data_path = os.path.join(os.getcwd(), "TestCities", city + ".csv")
    test_df = pd.read_csv(test_data_path)
    return test_df


def PreprocessingTestData(data):
    class Normalisation:
        def __init__(self):
            pass

        def time(self, time):
            return time / 24
        
        def temp(self, temp):
            mean = 13.0
            stdev = 9.869784
            return ((temp - mean) / stdev) / 3 # Assuming max temperature to be 40 degrees celsius
        
        def windspeed(self, speed):
            return (speed - 25) / 50
        
        def rainfall(self, rainfall):
            return rainfall / 20
        
        def humidity(self, humidity):
            return humidity / 120 
        
        def pressure(self, pressure):
            return (pressure - 1000) / 50
        
        def cloudcover(self, cover):
            return cover / 120

    normalizer = Normalisation()
    normalized_data = data.copy()
    normalized_data["time"] = normalizer.time(normalized_data["time"])
    normalized_data["tempC"] = normalizer.temp(normalized_data["tempC"])
    normalized_data["windspeed"] = normalizer.windspeed(normalized_data["windspeed"])
    normalized_data["rainfall"] = normalizer.rainfall(normalized_data["rainfall"])
    normalized_data["humidity"] = normalizer.humidity(normalized_data["humidity"])
    normalized_data["pressure"] = normalizer.pressure(normalized_data["pressure"])
    normalized_data["cloudcover"] = normalizer.cloudcover(normalized_data["cloudcover"])
    
    processed_data = []
    for i in range(len(normalized_data) - WindowSize + 1):
        window = normalized_data.iloc[i:i+WindowSize, 1:].values
        processed_data.append(window)
    
    return np.array(processed_data)

# Evaluate testing accuracy for a city
def ReturnMSE(model, test_data):
    predictions = model.predict(test_data)
    mse_per_sample = np.mean(np.square(predictions - test_data[:, -1, :]), axis=1)
    mean_mse = np.mean(mse_per_sample)
    return mean_mse


for city in cities:
    print(f"Evaluating mean square error for {city}...")
    
    model = LoadModel(city)
    test_data = LoadTestData(city)
    processed_test_data = PreprocessingTestData(test_data)
    
    mse = ReturnMSE(model, processed_test_data)
    
    print(f"Mean Square Error for {city}: {mse}")


