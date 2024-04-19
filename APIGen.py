import requests
import sys
import json

def GetRawWeatherFC(city):
    api_key = '7ff6b877d5bb47b08ad113553241604'

    try:
        url = "https://api.worldweatheronline.com/premium/v1/weather.ashx"
        params = {
            "key": api_key,
            "q": city,
            "format": "json",
            "num_of_days": 1,
            "cc": "no",
            "mca": "no",
            "tp": 1
        }
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        return data
    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("Please enter a valid city name")
        sys.exit("Please enter a valid city name")

def ParseRawWeatherFC(data): 
    # need city name, date, time, tempC, weatherDesc[value], windspeedKmph, rainfall, humidity, visibility, pressure, cloudcover, FeelsLikeC, icon
    weather_data = data['data']['weather'][0]['hourly']
    city = data['data']['request'][0]['query']
    Date = data['data']['weather'][0]['date']
    # print(f"City: {city}")
    # print(f"Date: {Date}")
    all_data = [city, Date]
    for hourly_data in weather_data:
        time = hourly_data['time']
        tempC = hourly_data['tempC']
        weatherDesc = hourly_data['weatherDesc'][0]['value']
        windspeedKmph = hourly_data['windspeedKmph']
        rainfall = hourly_data['precipMM']
        humidity = hourly_data['humidity']
        visibility = hourly_data['visibility']
        pressure = hourly_data['pressure']
        cloudcover = hourly_data['cloudcover']
        FeelsLikeC = hourly_data['FeelsLikeC']
        icon = hourly_data['weatherIconUrl'][0]['value']

        this_hour = {
            "time": f"{(int(time)//100):02d}:00",
            "weatherDesc": weatherDesc,
            "tempC": tempC,
            "FeelsLikeC": FeelsLikeC,
            "windspeedKmph": windspeedKmph,
            "rainfall": rainfall,
            "humidity": humidity,
            "visibility": visibility,
            "pressure": pressure,
            "cloudcover": cloudcover,
            "weatherIconUrl": icon
        }
        all_data.append(this_hour)

    return all_data

# print(GetRawWeatherFC("Singapore"))