import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.keras import layers
import keras
import os

NumFeatures = 7 
# order ['time', 'tempC', 'windspeed', 'rainfall', 'humidity', 'pressure', 'cloudcover']

WindowSize = 8
# number of previous records read to generate output

cities = ["shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata"]

def TrainCity(CityIndex, cities):
    
    citiesCSV = [os.getcwd() + "/Cities/" + city + ".csv" for city in cities]

    dfmain = pd.read_csv(citiesCSV[CityIndex])

    class Normalisation:
        def __init__(self):
            pass

        def time(self, time):
            return time / 24
        
        def temp(self, temp):
            mean = 13
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

    Normaliser = Normalisation()

    dfmain["time"] = dfmain["time"].map(Normaliser.time)
    dfmain["tempC"] = dfmain["tempC"].map(Normaliser.temp)
    dfmain["windspeed"] = dfmain["windspeed"].map(Normaliser.windspeed)
    dfmain["rainfall"] = dfmain["rainfall"].map(Normaliser.rainfall)
    dfmain["humidity"] = dfmain["humidity"].map(Normaliser.humidity)
    dfmain["pressure"] = dfmain["pressure"].map(Normaliser.pressure)
    dfmain["cloudcover"] = dfmain["cloudcover"].map(Normaliser.cloudcover)

    df = dfmain.drop(columns=["date"])

    def SlidingWindow(TimeSeries, WindowSize):
        SplitSeries = []
        for i in range(len(TimeSeries) - WindowSize + 1):
            SplitSeries.append(TimeSeries[i : i + WindowSize].tolist())
        return SplitSeries

    # RNN input format: 3d tensor of the shape < None, SlidingWindowSizeWindow, NumFeatures >

    print("Collecting and processing data ...")

    ListFeatures = []

    for i in range(1, NumFeatures + 1): 
        ListFeatures.append(SlidingWindow(dfmain.iloc[:,i], WindowSize))

    WeatherData = []

    for t in range(len(ListFeatures[0])):
        WeatherData.append([[ListFeatures[i][t][k] for i in range(NumFeatures)] for k in range(WindowSize)])

    WeatherData = tf.constant(WeatherData)

    # Keras sequential model with stacked Gated Recurrent (GRU) units
    WeatherModel = keras.Sequential()

    inputs = keras.Input(shape = (None, WindowSize - 1, NumFeatures))

    # Increased capacity GRU architecture
    WeatherModel.add(tf.keras.layers.GRU(128, return_sequences=True))
    WeatherModel.add(tf.keras.layers.GRU(128))
    WeatherModel.add(tf.keras.layers.Dense(512, activation='relu'))
    WeatherModel.add(tf.keras.layers.Dense(7, activation='tanh'))

    WeatherModel.build(input_shape=(None, WindowSize - 1, NumFeatures))

    WeatherModel.summary()

    WeatherModel.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),  # Adjusted learning rate
                loss=tf.keras.losses.mean_squared_error,
                metrics=['accuracy', 'mean_squared_error'])

    x_train = WeatherData[:,:-1,:]
    y_train = WeatherData[:,-1, :]

    print("Model training starting ...")

    history = WeatherModel.fit(x_train, y_train, batch_size=16, epochs=30)

    # Save the model to a checkpoint
    WeatherModel.save_weights(os.getcwd() + "/Checkpoints/" + cities[CityIndex] + "Checkpoint")

    print(f"Finished saving checkpoint for {cities[CityIndex]}.")

for i in range(len(cities)):
    TrainCity(i, cities)