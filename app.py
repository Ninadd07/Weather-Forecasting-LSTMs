import streamlit as st
from weather_functions import AIInput, GetNearestTime, GetImage

st.set_page_config(page_title="WeatherWise", page_icon="icons/weather.ico")

cities = ("shanghai", "beijing", "moscow", "karachi", "singapore", "london", "madrid", "berlin", "paris", "sydney", "rome", "toronto", "seoul", "dubai", "delhi", "mumbai", "pune", "bangalore", "chennai", "kolkata")

city_options = tuple(["Select option"] + [city.title() for city in cities])

if 'timetemp' not in st.session_state:
    st.session_state.timetemp = 18

st.session_state.time = st.session_state.timetemp

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def clicked():
    st.session_state.clicked = True

time = st.slider("Time", 0, 23, 1, key='time')
time12hr = time % 12
if time12hr == time:
    time12hr = f"{time12hr:02d}:00 am"
else:
    time12hr = f"{time12hr:02d}:00 pm"

city_option = st.selectbox(
    "Which city?", 
    city_options
)

city = city_option.lower()

clicked = st.button("Get weather", on_click=clicked)

if st.session_state.clicked:
    weather_data = AIInput(city)
    if time < 2:
        data = weather_data[0]
        prev_data = data.copy()
    else:
        for x in range(len(weather_data)) :
            if weather_data[x]['time'] == GetNearestTime(time):
                data = weather_data[x]
                if x == 0:
                    prev_data = data.copy()
                else:
                    prev_data = weather_data[x-1]
                break

    st.write(f"""
        # Weather Forecast
        ## For {city_option}, at {time:02d}:00 ({time12hr})
    """)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{data['tempC']} ºC", f"{data['tempC']-prev_data['tempC']} ºC")
    c2.metric("Wind Speed", f"{data['windspeedKmph']} kmph", f"{data['windspeedKmph']-prev_data['windspeedKmph']} km/h")
    c3.metric("Precipitation", f"{data['rainfall']} mm", f"{data['rainfall']-prev_data['rainfall']} mm")
    c1.metric("Humidity", f"{data['humidity']} %", f"{data['humidity']-prev_data['humidity']} %")
    c2.metric("Pressure", f"{data['pressure']} mb", f"{data['pressure']-prev_data['pressure']} mb")
    c3.metric("Cloud cover", f"{data['cloudcover']} %", f"{data['cloudcover']-prev_data['cloudcover']} %")
    c4.image(GetImage(time, data['rainfall'], data['cloudcover']))
    c4.write("")
    c4.write("")
    c4.write("")

    if st.session_state.time > 2:
        if c1.button("Go back 3 hours"):
            st.session_state.timetemp = st.session_state.timetemp - 3
            print(st.session_state.timetemp)
    if st.session_state.time < 21:    
        if c4.button("Go forward 3 hours"):
            st.session_state.timetemp = st.session_state.timetemp + 3
            print(st.session_state.timetemp)