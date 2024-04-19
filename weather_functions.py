from APIGen import ParseRawWeatherFC, GetRawWeatherFC
from main import GetNextWeather
import streamlit as st

@st.cache_data
def AIInput(city):
    if city == "Select option":
        return None

    api_weather_data = ParseRawWeatherFC(GetRawWeatherFC("+".join(city.split()))) 
    # [cityname, date, {hourly weather data}]
    ai_weather_data = []

    city = "".join(city.split())

    cities = ["shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata"]

    if city in cities:
        for hr in range(0, 24, 3):
            ai_input_data = [api_weather_data[hr+2]['time'][:2],
                            api_weather_data[hr+2]['tempC'],
                            api_weather_data[hr+2]['windspeedKmph'],
                            api_weather_data[hr+2]['rainfall'],
                            api_weather_data[hr+2]['humidity'],
                            api_weather_data[hr+2]['pressure'],
                            api_weather_data[hr+2]['cloudcover']
            ]

            ai_input_data = [float(ai_input_data[x]) for x in range(len(ai_input_data))]

            # model accessing goes here (output a list)
            hourly_ai_dict = GetNextWeather(cities.index(city), ai_input_data)
            hourly_ai_dict['time'] = int(hourly_ai_dict['time'])
            ai_weather_data.append(hourly_ai_dict.copy())
            hourly_ai_dict.clear()
            ai_input_data.clear()
            
    return ai_weather_data

def GetNearestTime(time):
    if time % 3 == 1:
        time -= 1
    elif time % 3 == 2:
        time += 1
    
    return time

def GetImage(time, precipitation, cloud):
    classes = ["sunny", "rain", "cloudy", "night", "twonightclouds", "nightcloudy", "suncloudy"]

    classes = [w + ".png" for w in classes]
    
    if time < 6 or time > 19: # Night
        if precipitation != 0:
            weather = 1
        elif cloud < 15:
            weather = 3
        elif cloud > 75:
            weather = 4
        else:
            weather = 5
    else:
        if precipitation != 0:
            weather = 1
        elif cloud < 25:
            weather = 0
        elif cloud > 75:
            weather = 2
        else:
            weather = 6

    return "icons/" + classes[weather]
