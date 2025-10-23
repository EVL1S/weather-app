#Weather App
from datetime import datetime, timedelta
import requests
import locale
from wmo import wmo as WMO 


userInput_city = input('Zadej město: ')
url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={userInput_city}&count=1&language=cs&format=json"
response = requests.get(url_geo)
data = response.json()

if "results" not in data:
    print(f'Město "{userInput_city}" nenalezeno.')
    exit()

lat = data["results"][0]["latitude"]
lon = data["results"][0]["longitude"]
locale.setlocale(locale.LC_TIME, "cs_CZ.UTF-8")

url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,apparent_temperature&daily=temperature_2m_min,temperature_2m_max,weather_code&forecast_days=3&timezone=Europe/Prague"
weather_response = requests.get(url_weather)
weather_data = weather_response.json()

temp = weather_data["current"]["temperature_2m"]
apparent = weather_data["current"]["apparent_temperature"]
temp_unit = weather_data["current_units"]["temperature_2m"]
temp_min = weather_data['daily']['temperature_2m_min']
temp_max = weather_data['daily']['temperature_2m_max']
wind_speed = weather_data["current"]["wind_speed_10m"]
wind_unit = weather_data["current_units"]["wind_speed_10m"]
weather_code = weather_data['daily']['weather_code']
timezone = weather_data['timezone']
timezone_abbreviation = weather_data['timezone_abbreviation']
time = datetime.fromisoformat(weather_data['current']['time'])
next_day = (time + timedelta(days=1))
day_after = (time + timedelta(days=2))
elevation = weather_data['elevation']
wmo0 = WMO.get(int(weather_code[0]), f"Neznámý jev (kód: {weather_code[0]})")
wmo1 = WMO.get(int(weather_code[1]), f"Neznámý jev (kód: {weather_code[1]})")
wmo2 = WMO.get(int(weather_code[2]), f"Neznámý jev (kód: {weather_code[2]})")

print("\n", weather_data, "\n")

def printWeather():
    return f"""
🌦️  Počasí pro: {userInput_city}
📍 Souřadnice: {lat}, {lon}     🗺️  Časová zóna: {timezone} ({timezone_abbreviation})
---------------------------------------------------------------------------

🕒 Aktuálně - {time.strftime("%d. %B %Y, %H:%M")}
🌡️  Teplota: {temp} {temp_unit}  {"🥶" if apparent < temp else "🥵"} Pocitová teplota: {apparent} {temp_unit}
{wmo0}
💨 Vítr: {wind_speed} {wind_unit}
🏔️  Nadmořská výška: {round(elevation)} m

📅 Předpověď na 3 dny
---------------------------------------------------------------------------
🗓️  {time.strftime("%A")[:2]} {time.strftime("%d.%m.")}   🌦️  min: {temp_min[0]} {temp_unit}   max: {temp_max[0]} {temp_unit}   {wmo0}
🗓️  {next_day.strftime("%A")[:2]} {next_day.strftime("%d.%m.")}   🌧️  min: {temp_min[1]} {temp_unit}   max: {temp_max[1]} {temp_unit}   {wmo1}
🗓️  {day_after.strftime("%A")[:2]} {day_after.strftime("%d.%m.")}   🌩️  min: {temp_min[2]} {temp_unit}   max: {temp_max[2]} {temp_unit}   {wmo2}
---------------------------------------------------------------------------
"""


print(printWeather())
