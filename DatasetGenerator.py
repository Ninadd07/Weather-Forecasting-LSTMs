import requests
import csv

cities = ["shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata"]



for city in cities:
    file = open(f"lol/{city}.csv", "a+", newline = "")
    writer = csv.writer(file)
    writer.writerow(["date", "time", "tempC", "windspeed", "rainfall", "humidity", "pressure", "cloudcover"])

    api_key = "7ff6b877d5bb47b08ad113553241604"

    for i in range(1, 13):
        if i == 2:
            response = requests.get(f"https://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={city}&date=2023-{i:02d}-01&enddate=2023-{i:02d}-28&format=json&key={api_key}")
        elif i in [1, 3, 5, 7, 8, 10, 12]:
            response = requests.get(f"https://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={city}&date=2023-{i:02d}-01&enddate=2023-{i:02d}-31&format=json&key={api_key}")
        else:
            response = requests.get(f"https://api.worldweatheronline.com/premium/v1/past-weather.ashx?q={city}&date=2023-{i:02d}-01&enddate=2023-{i:02d}-30&format=json&key={api_key}")
        data = response.json()["data"]["weather"]
        all_days = []
        for day in data:
            this_day = []
            for j in range(len(day["hourly"])):
                hour = int(day["hourly"][j]["time"]) // 100
                if not hour % 3 == 0:
                    continue
                datapoint = [
                    day["date"],
                    f"{hour:02d}",
                    day["hourly"][j]["tempC"],
                    day["hourly"][j]["windspeedKmph"],
                    day["hourly"][j]["precipMM"],
                    day["hourly"][j]["humidity"],
                    day["hourly"][j]["pressure"],
                    day["hourly"][j]["cloudcover"]
                ]
                this_day.append(datapoint)
            all_days.append(this_day)
        
        #[[[12am], [3am], [6am], [9am],] x 31]
        for day in all_days : 
            writer.writerows(day)


    file.close()