import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import ttkbootstrap

def get_weather(city):
    API_KEY = "26da47f536ad060fb62d3bde1ddb3e35"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    weather = res.json()
    temperature = weather['main']['temp'] - 273.15
    humidity = weather['main']['humidity']
    weather_conditions = weather['weather'][0]['description']
    icon_id = weather['weather'][0]['icon']
    city = weather['name']
    country = weather['sys']['country']

    icon_url = f'https://openweathermap.org/img/wn/{icon_id}@2x.png'

    # Return the weather details as a tuple
    return icon_url, temperature, humidity,weather_conditions, city, country

def search():
    city = city_entry.get()
    result = get_weather(city)
    
    if result is None:
        return

    icon_url, temperature,Humidity, description, city, country = result
    location_label.configure(text=f"{city}, {country}")
    
    # Download and display the weather icon
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Conditions: {description}")
    Humidity_label.configure(text=f"Humidity: {Humidity}%")

# GUI setup
root = ttkbootstrap.Window(themename="morph")
root.title("WeatherApp")
root.geometry("400x400")

city_entry = ttkbootstrap.Entry(root, font=('Helvetica', 18))
city_entry.pack(pady=10)

search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle='warning')
search_button.pack(pady=10)

location_label = tk.Label(root,font='Helvetica 25 bold')
location_label.pack(pady=20)

icon_label = tk.Label(root)
icon_label.pack()

temperature_label = tk.Label(root, font='Helvetica 20 bold')
temperature_label.pack()

description_label = tk.Label(root, font='Helvetica 20 bold')
description_label.pack()

Humidity_label = tk.Label(root, font='Helvetica 20 bold')
Humidity_label.pack()
root.mainloop()
