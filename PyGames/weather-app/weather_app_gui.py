import os
import tkinter as tk
from tkinter import messagebox
import requests

BG_COLOR = "#0f172a"
CARD_COLOR = "#020617"
TEXT_COLOR = "#e5e7eb"
ACCENT_COLOR = "#22c55e"
FONT_NORMAL = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_RESULT = ("Segoe UI", 11, "bold")

API_KEY = "137d0df46e535b17c2008db2d001346e"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    result_label.config(text="Loading...", fg=TEXT_COLOR)
    root.update()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("cod") != 200:
            result_label.config(text=f"Error: {data.get('message', 'City not found')}", fg="#ef4444")
            return

        city_name = data["name"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        desc = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        result_text = f"""City: {city_name}
Temp: {temp}°C (feels {feels}°C)
Humidity: {humidity}%
Wind: {wind} m/s
Condition: {desc.title()}"""

        result_label.config(text=result_text, fg=ACCENT_COLOR)

    except requests.exceptions.Timeout:
        result_label.config(text="Error: Request timeout", fg="#ef4444")
    except requests.exceptions.ConnectionError:
        result_label.config(text="Error: No internet connection", fg="#ef4444")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="#ef4444")

root = tk.Tk()
root.title("Weather App - BSc IT Project")
root.geometry("480x320")
root.minsize(400, 280)
root.configure(bg=BG_COLOR)

# Top bar
top_bar = tk.Frame(root, bg=BG_COLOR)
top_bar.pack(fill="x", pady=(8, 0))

title_label = tk.Label(top_bar, text="Weather App", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_COLOR)
title_label.pack(side="left", padx=16)

subtitle_label = tk.Label(top_bar, text="Python + OpenWeather API", font=("Segoe UI", 9), bg=BG_COLOR, fg="#9ca3af")
subtitle_label.pack(side="left", padx=8)

# Card container
card_outer = tk.Frame(root, bg=BG_COLOR)
card_outer.pack(fill="both", expand=True, padx=16, pady=12)

card = tk.Frame(card_outer, bg=CARD_COLOR, bd=0, highlightthickness=1, highlightbackground="#1f2937")
card.pack(fill="both", expand=True)

# Form area
form_frame = tk.Frame(card, bg=CARD_COLOR)
form_frame.pack(padx=15, pady=15, fill="x")

city_label = tk.Label(form_frame, text="City:", font=FONT_NORMAL, bg=CARD_COLOR, fg=TEXT_COLOR)
city_label.grid(row=0, column=0, padx=5, pady=8, sticky="e")

city_entry = tk.Entry(form_frame, width=20, font=FONT_NORMAL, relief="flat")
city_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")
city_entry.insert(0, "Delhi")

# Button
button_frame = tk.Frame(card, bg=CARD_COLOR)
button_frame.pack(pady=5)

search_button = tk.Button(button_frame, text="Search", command=get_weather, width=15, font=FONT_NORMAL,
                          bg=ACCENT_COLOR, fg="white", activebackground="#16a34a", relief="flat", cursor="hand2")
search_button.pack(pady=5)

# Result area
result_frame = tk.Frame(card, bg=CARD_COLOR)
result_frame.pack(padx=15, pady=(0, 15), fill="both", expand=True)

result_label = tk.Label(result_frame, text="Enter a city and click Search", font=FONT_RESULT, bg=CARD_COLOR,
                        fg="#9ca3af", justify="left", wraplength=280)
result_label.pack(pady=5)

root.mainloop()
