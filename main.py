# Upload the checkpoint data to the model

import tensorflow as tf
import keras
import os
from pathlib import Path

def GetNextWeather(CityIndex, CurrentParamsList): # CurrentParamsList
    cities = ["shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata"]
    
    NumFeatures = 7
    WindowSize = 2

    WeatherModel = keras.Sequential()

    inputs = keras.Input(shape=(None, WindowSize - 1, NumFeatures))

    # Simplified GRU architecture with fewer neurons
    WeatherModel.add(tf.keras.layers.GRU(128, return_sequences=True))
    WeatherModel.add(tf.keras.layers.GRU(128))
    WeatherModel.add(tf.keras.layers.Dense(512, activation='relu'))
    WeatherModel.add(tf.keras.layers.Dense(7, activation='tanh'))

    WeatherModel.build(input_shape=(None, WindowSize - 1, NumFeatures))

    model = tf.keras.models.clone_model(WeatherModel)
    checkpoint = tf.train.Checkpoint(model)
    directory = str(Path(os.getcwd() + "/Checkpoints/"))
    checkpoint.restore(directory + "/" + cities[CityIndex] + "Checkpoint").expect_partial()


    #eg path : C:\Users\manas\Documents\IE0005_Project\Checkpoints\beijingCheckpoint.data-00000-of-00001

    class Renormalisation:
        def __init__(self):
            pass

        def time(self, time):
            return time * 24
        
        def temp(self, temp):
            mean = 13
            stdev = 9.869784
            return (temp * stdev * 3) + mean # Assuming max temperature to be 40 degrees celsius
        
        def windspeed(self, speed):
            return (speed * 50) + 25
        
        def rainfall(self, rainfall):
            return rainfall * 20
        
        def humidity(self, humidity):
            return humidity * 120 
        
        def pressure(self, pressure):
            return (pressure * 50) + 1000
        
        def cloudcover(self, cover):
            return cover * 120
        
        def Renormalise(self, y_pred): # The input has to be a list or numpy array
            y_pred[0] = self.time(y_pred[0])
            y_pred[1] = self.temp(y_pred[1])
            y_pred[2] = self.windspeed(y_pred[2])
            y_pred[3] = self.rainfall(y_pred[3])
            y_pred[4] = self.humidity(y_pred[4])
            y_pred[5] = self.pressure(y_pred[5])
            y_pred[6] = self.cloudcover(y_pred[6])
            
            return y_pred

    class Normalisation:
        def __init__(self):
            pass

        def time(self, time):
            return time / 24
        
        def temp(self, temp):
            mean = 13.0
            stdev = 9.869784
            return ( (temp - mean) / stdev ) / 3 # Assuming max temperature to be 40 degrees celsius
        
        def windspeed(self, speed):
            return ( speed - 25) / 50
        
        def rainfall(self, rainfall):
            return rainfall / 20
        
        def humidity(self, humidity):
            return humidity / 120 
        
        def pressure(self, pressure):
            return (pressure - 1000) / 50
        
        def cloudcover(self, cover):
            return cover / 120
        
        def Normalise(self, inp): # The input must be a float tensor
            op = [0] * 7

            op[0] = self.time(inp[0])
            op[1] = self.temp(inp[1])
            op[2] = self.windspeed(inp[2])
            op[3] = self.rainfall(inp[3])
            op[4] = self.humidity(inp[4])
            op[5] = self.pressure(inp[5])
            op[6] = self.cloudcover(inp[6]) 

            return tf.stack(op)       

    renormaliser = Renormalisation()
    normaliser = Normalisation()

    CurrentWeather = normaliser.Normalise(tf.constant(CurrentParamsList, dtype=tf.float32))

    ModelInp = tf.reshape(CurrentWeather, [1,1,7])
    ModelOp = model.predict((ModelInp))[0]

    NextWeather = renormaliser.Renormalise(ModelOp)

    NextWeather = [abs(int(NextWeather[i])) for i in range(len(NextWeather))]

    NextWeather[0] = CurrentParamsList[0] + 3

    NextWeather = {'time': NextWeather[0],
                   'tempC': NextWeather[1],
                   'windspeedKmph': NextWeather[2],
                   'rainfall': NextWeather[3],
                   'humidity': NextWeather[4],
                   'pressure': NextWeather[5],
                   'cloudcover': NextWeather[6]}

    return NextWeather

# GetNextWeather(CityIndex, [0, 29, 10, 0.2, 75, 1010, 84]) : a sample way to call the input