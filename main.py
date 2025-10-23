#Weather App
from datetime import datetime, timedelta
import requests
import locale
from wmo import wmo as WMO 
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Weather App (V3.0 - GUI)")
root.geometry("640x480")

city_var = tk.StringVar(value="Brno")

container = ttk.Frame(root, padding=12)
container.pack(fill="both", expand=True)

row = ttk.Frame(container)
row.pack(fill="x", pady=(0,8))


def on_fetch():
    city = city_var.get().strip()

    url_geo = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=cs&format=json"
    response = requests.get(url_geo)
    data = response.json()

    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]

    url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,apparent_temperature&daily=temperature_2m_min,temperature_2m_max,weather_code&forecast_days=3&timezone=auto"
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


    set_output(printWeather(city, lat, lon, timezone, timezone_abbreviation, time, temp, temp_unit, apparent, wind_speed, wind_unit, elevation, next_day, day_after, temp_min, temp_max, wmo0, wmo1, wmo2))




ttk.Label(row, text="Město: ").pack(side="left")
city_entry = ttk.Entry(row, textvariable=city_var, width=28)
city_entry.pack(side="left", padx=8)

locale.setlocale(locale.LC_TIME, "cs_CZ.UTF-8")

def printWeather(city, lat, lon, timezone, timezone_abbreviation, time, temp, temp_unit, apparent, wind_speed, wind_unit, elevation, next_day, day_after, temp_min, temp_max, wmo0, wmo1, wmo2):
    return f"""
🌦️  Počasí pro: {city}
📍 Souřadnice: {lat}, {lon}  🗺️  Časová zóna: {timezone} ({timezone_abbreviation})
----------------------------------------------------------------------------

🕒 Aktuálně - {time.strftime("%d. %B %Y, %H:%M")}
🌡️  Teplota: {temp} {temp_unit}  {"🥶" if apparent < temp else "🥵"} Pocitová teplota: {apparent} {temp_unit}
{wmo0}
💨 Vítr: {wind_speed} {wind_unit}
🏔️  Nadmořská výška: {round(elevation)} m

📅 Předpověď na 3 dny
----------------------------------------------------------------------------
🗓️  {time.strftime("%A")[:2]} {time.strftime("%d.%m.")}   min: {temp_min[0]} {temp_unit}   max: {temp_max[0]} {temp_unit}   {wmo0}
🗓️  {next_day.strftime("%A")[:2]} {next_day.strftime("%d.%m.")}   min: {temp_min[1]} {temp_unit}   max: {temp_max[1]} {temp_unit}   {wmo1}
🗓️  {day_after.strftime("%A")[:2]} {day_after.strftime("%d.%m.")}   min: {temp_min[2]} {temp_unit}   max: {temp_max[2]} {temp_unit}   {wmo2}
----------------------------------------------------------------------------
"""

ttk.Button(row, text="Hledat", command=on_fetch).pack(side="left")

output = tk.Text(container, height=12, wrap="word")
output.pack(fill="both", expand=True)

def set_output(text: str):
    output.config(state="normal")
    output.delete("1.0", "end")
    output.insert("1.0", text)
    output.config(state="disabled")

city_entry.focus_set()
root.bind("<Return>", lambda e: on_fetch())

root.mainloop()


