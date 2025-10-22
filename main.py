#Weather App

import requests


userInput_city = input('Zadej město: ')
url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={userInput_city}&count=1&language=cs&format=json"
response = requests.get(url_geo)
data = response.json()

if "results" not in data:
    print(f'Město "{userInput_city}" nenalezeno.')
    exit()

lat = data["results"][0]["latitude"]
lon = data["results"][0]["longitude"]

url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,apparent_temperature&daily=temperature_2m_min,temperature_2m_max,weather_code&forecast_days=3&timezone=Europe/Prague"
weather_response = requests.get(url_weather)
weather_data = weather_response.json()

temp = weather_data["current"]["temperature_2m"]
temp_unit = weather_data["current_units"]["temperature_2m"]
wind_speed = weather_data["current"]["wind_speed_10m"]
wind_unit = weather_data["current_units"]["wind_speed_10m"]


def getWeather(c, t, tu, w, wu):
    return f"Počasí pro {c}\n{t} {tu}\n{w} {wu}"


print(getWeather(userInput_city, temp, temp_unit, wind_speed, wind_unit))
