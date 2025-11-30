import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import pyjokes
import subprocess
import platform
import requests
from pygame import mixer
import time
import random

# ============ INITIALIZATION ============
class AdvancedVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced AI Voice Assistant")
        self.root.geometry("1100x750")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#0a0e27"
        self.accent_color = "#00d4ff"
        self.text_color = "#ffffff"
        self.root.config(bg=self.bg_color)
        
        # Initialize TTS engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.stop_listening = False
        
        # Weather API (using free API - Open-Meteo)
        self.weather_api = "https://api.open-meteo.com/v1/forecast"
        
        # Create GUI
        self.create_gui()
    
    def create_gui(self):
        """Create the user interface"""
        
        # ====== HEADER ======
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🤖 ADVANCED AI VOICE ASSISTANT", 
                               font=("Arial", 22, "bold"), bg=self.accent_color, fg="black")
        title_label.pack(pady=15)
        
        # ====== STATUS DISPLAY ======
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_label = tk.Label(status_frame, text="🟢 Ready", 
                                     font=("Arial", 14, "bold"), 
                                     fg=self.accent_color, bg=self.bg_color)
        self.status_label.pack()
        
        # ====== COMMAND LOG ======
        log_frame = tk.Frame(self.root, bg=self.bg_color)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        log_label = tk.Label(log_frame, text="📝 Command Log:", 
                            font=("Arial", 12, "bold"), 
                            fg=self.text_color, bg=self.bg_color)
        log_label.pack(anchor="w")
        
        self.text_display = scrolledtext.ScrolledText(log_frame, 
                                                      width=130, height=15,
                                                      bg="#1a1f3a", 
                                                      fg=self.accent_color,
                                                      font=("Courier", 10),
                                                      insertbackground=self.accent_color)
        self.text_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Configure tags for styling
        self.text_display.tag_config("assistant", foreground="#00ff00")
        self.text_display.tag_config("user", foreground="#00d4ff")
        self.text_display.tag_config("error", foreground="#ff6b6b")
        self.text_display.tag_config("info", foreground="#ffd700")
        
        # ====== BUTTON FRAME 1 ======
        button_frame1 = tk.Frame(self.root, bg=self.bg_color)
        button_frame1.pack(fill=tk.X, padx=20, pady=8)
        
        # Start Button
        self.start_button = tk.Button(button_frame1, text="🎤 START LISTENING", 
                                     command=self.start_listening_thread,
                                     font=("Arial", 11, "bold"),
                                     bg=self.accent_color, fg="black",
                                     padx=15, pady=8, relief=tk.RAISED, 
                                     cursor="hand2", width=15)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop Button
        self.stop_button = tk.Button(button_frame1, text="⏹️ STOP", 
                                    command=self.stop_listening_action,
                                    font=("Arial", 11, "bold"),
                                    bg="#ff6b6b", fg="black",
                                    padx=15, pady=8, relief=tk.RAISED,
                                    cursor="hand2", state=tk.DISABLED, width=15)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Clear Button
        clear_button = tk.Button(button_frame1, text="🗑️ CLEAR LOG", 
                                command=self.clear_log,
                                font=("Arial", 11, "bold"),
                                bg="#666", fg="white",
                                padx=15, pady=8, relief=tk.RAISED,
                                cursor="hand2", width=15)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Test Joke Button
        joke_button = tk.Button(button_frame1, text="😂 TELL JOKE", 
                               command=self.tell_joke_direct,
                               font=("Arial", 11, "bold"),
                               bg="#ff9500", fg="black",
                               padx=15, pady=8, relief=tk.RAISED,
                               cursor="hand2", width=15)
        joke_button.pack(side=tk.LEFT, padx=5)
        
        # Exit Button
        exit_button = tk.Button(button_frame1, text="❌ EXIT", 
                               command=self.exit_app,
                               font=("Arial", 11, "bold"),
                               bg="#8b0000", fg="white",
                               padx=15, pady=8, relief=tk.RAISED,
                               cursor="hand2", width=15)
        exit_button.pack(side=tk.RIGHT, padx=5)
        
        # ====== BUTTON FRAME 2 - QUICK ACTIONS ======
        button_frame2 = tk.Frame(self.root, bg=self.bg_color)
        button_frame2.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(button_frame2, text="Quick Actions:", font=("Arial", 10, "bold"), 
                fg=self.accent_color, bg=self.bg_color).pack(side=tk.LEFT, padx=5)
        
        # Quick action buttons
        tk.Button(button_frame2, text="📝 Open Notepad", command=self.open_notepad,
                 font=("Arial", 9), bg="#228b22", fg="white", padx=10, pady=5,
                 cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(button_frame2, text="🧮 Open Calculator", command=self.open_calculator,
                 font=("Arial", 9), bg="#228b22", fg="white", padx=10, pady=5,
                 cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(button_frame2, text="🌤️ Get Weather", command=self.get_weather_direct,
                 font=("Arial", 9), bg="#1e90ff", fg="white", padx=10, pady=5,
                 cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        tk.Button(button_frame2, text="🎵 Play Music", command=self.play_music,
                 font=("Arial", 9), bg="#9932cc", fg="white", padx=10, pady=5,
                 cursor="hand2").pack(side=tk.LEFT, padx=3)
        
        # ====== INFO FRAME ======
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(fill=tk.X, padx=20, pady=5)
        
        info_text = tk.Label(info_frame, 
                            text="💡 Voice Commands: 'time', 'date', 'open google', 'tell joke', 'weather in Delhi', 'open notepad', 'calculator', 'play music', 'search wikipedia', 'exit'",
                            font=("Arial", 9), fg="#aaa", bg=self.bg_color, wraplength=1000, justify=tk.LEFT)
        info_text.pack(anchor="w")
        
        self.log_message("Advanced Assistant Started ✓", "info")
    
    # ============ UTILITY METHODS ============
    def log_message(self, message, tag="info"):
        """Log a message to the display"""
        self.text_display.insert(tk.END, message + "\n", tag)
        self.text_display.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """Clear the command log"""
        self.text_display.delete(1.0, tk.END)
    
    def speak_and_log(self, text):
        """Speak text and log it"""
        self.log_message(f"🤖 Assistant: {text}", "assistant")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def exit_app(self):
        """Exit the application"""
        self.root.destroy()
    
    # ============ LISTENING METHODS ============
    def start_listening_thread(self):
        """Start listening in a separate thread"""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_listening = True
        self.stop_listening = False
        self.status_label.config(text="🔴 Listening...", fg="#ff6b6b")
        
        thread = threading.Thread(target=self.listen_and_process)
        thread.daemon = True
        thread.start()
    
    def stop_listening_action(self):
        """Stop listening"""
        self.stop_listening = True
        self.is_listening = False
        self.status_label.config(text="🟡 Processing...", fg="#ffd700")
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
    
    def listen_and_process(self):
        """Listen for voice commands and process them"""
        try:
            with sr.Microphone() as source:
                self.log_message("🎤 Listening for command...", "info")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10)
                self.log_message("🔄 Processing...", "info")
                command = self.recognizer.recognize_google(audio, language='en-in')
                self.log_message(f"👤 You: {command}", "user")
                self.process_command(command.lower())
                
        except sr.UnknownValueError:
            self.log_message("❌ Sorry, I didn't understand that. Please try again.", "error")
        except sr.RequestError:
            self.log_message("❌ Internet connection error. Please check your connection.", "error")
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}", "error")
        finally:
            self.status_label.config(text="🟢 Ready", fg=self.accent_color)
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    # ============ FEATURE: TELL JOKES ============
    def tell_joke_direct(self):
        """Direct button to tell joke"""
        thread = threading.Thread(target=self.tell_joke)
        thread.daemon = True
        thread.start()
    
    def tell_joke(self):
        """Tell a random joke"""
        try:
            try:
                joke = pyjokes.get_joke(category='programming', language='en')
            except:
                try:
                    joke = pyjokes.get_joke(language='en')
                except:
                    # Fallback to manual jokes
                    manual_jokes = [
                        "Why do programmers prefer dark mode? Because light attracts bugs!",
                        "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                        "Why did the developer go broke? Because he used up all his cache!",
                        "What's a programmer's favorite place to hang out? Foo Bar!",
                        "Why do Java developers wear glasses? Because they can't C sharp!",
                        "How do you know if there's an engineer in your bathroom? He looks at the instructions on the shampoo bottle!",
                        "Why did the programmer quit his job? Because he didn't get arrays!",
                        "What do you call a programmer from Finland? Nerdic!",
                        "Why do programmers always mix up Halloween and Christmas? Because Oct 31 equals Dec 25!",
                        "How many MySQL DBAs does it take to change a lightbulb? Three: one to change it and two to discuss how much better the old one was."
                    ]
                    joke = random.choice(manual_jokes)
            
            self.log_message(f"😂 Joke: {joke}", "assistant")
            self.engine.say(joke)
            self.engine.runAndWait()
        except Exception as e:
            self.log_message(f"❌ Error telling joke: {str(e)}", "error")
    
    # ============ FEATURE: OPEN NOTEPAD ============
    def open_notepad(self):
        """Open Notepad application"""
        try:
            if platform.system() == 'Windows':
                os.startfile('notepad.exe')
                self.speak_and_log("Opening Notepad...")
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', '-a', 'TextEdit'])
                self.speak_and_log("Opening TextEdit...")
            else:  # Linux
                subprocess.Popen(['gedit'])
                self.speak_and_log("Opening Text Editor...")
        except Exception as e:
            self.log_message(f"❌ Error opening notepad: {str(e)}", "error")
    
    # ============ FEATURE: OPEN CALCULATOR ============
    def open_calculator(self):
        """Open Calculator application"""
        try:
            if platform.system() == 'Windows':
                os.startfile('calc.exe')
                self.speak_and_log("Opening Calculator...")
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', '-a', 'Calculator'])
                self.speak_and_log("Opening Calculator...")
            else:  # Linux
                subprocess.Popen(['gnome-calculator'])
                self.speak_and_log("Opening Calculator...")
        except Exception as e:
            self.log_message(f"❌ Error opening calculator: {str(e)}", "error")
    
    # ============ FEATURE: WEATHER ============
    def get_weather_direct(self):
        """Direct button to get weather"""
        thread = threading.Thread(target=lambda: self.get_weather("New Delhi"))
        thread.daemon = True
        thread.start()
    
    def get_weather(self, city):
        """Get weather information using free Open-Meteo API"""
        try:
            self.log_message(f"🌤️ Getting weather for {city}...", "info")
            
            # Coordinates for common cities
            cities = {
                'delhi': (28.6139, 77.2090),
                'mumbai': (19.0760, 72.8777),
                'bangalore': (12.9716, 77.5946),
                'hyderabad': (17.3850, 78.4867),
                'kolkata': (22.5726, 88.3639),
                'new delhi': (28.6139, 77.2090),
                'london': (51.5074, -0.1278),
                'new york': (40.7128, -74.0060),
                'paris': (48.8566, 2.3522),
                'tokyo': (35.6762, 139.6503),
                'sydney': (-33.8688, 151.2093),
                'toronto': (43.6532, -79.3832),
                'dubai': (25.2048, 55.2708),
                'singapore': (1.3521, 103.8198)
            }
            
            city_lower = city.lower()
            if city_lower in cities:
                lat, lon = cities[city_lower]
                params = {
                    'latitude': lat,
                    'longitude': lon,
                    'current': 'temperature_2m,weather_code,wind_speed_10m'
                }
                
                response = requests.get(self.weather_api, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    current = data['current']
                    temp = current['temperature_2m']
                    wind = current['wind_speed_10m']
                    weather_code = current['weather_code']
                    
                    # Weather descriptions
                    weather_desc = self.get_weather_description(weather_code)
                    
                    weather_info = f"🌤️ {city.title()}: {temp}°C, {weather_desc}, Wind: {wind} km/h"
                    self.log_message(f"🤖 Assistant: {weather_info}", "assistant")
                    self.engine.say(f"Weather in {city}. Temperature is {temp} degrees. {weather_desc}. Wind speed is {wind} kilometers per hour.")
                    self.engine.runAndWait()
                else:
                    self.log_message("❌ Could not fetch weather data", "error")
            else:
                self.log_message(f"❌ City '{city}' not found in database. Try: Delhi, Mumbai, London, New York, Tokyo, etc.", "error")
                
        except Exception as e:
            self.log_message(f"❌ Error getting weather: {str(e)}", "error")
    
    def get_weather_description(self, code):
        """Get weather description from WMO code"""
        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return descriptions.get(code, "Unknown weather")
    
    # ============ FEATURE: PLAY MUSIC ============
    def play_music(self, song_path=None):
        """Play music from YouTube or local file"""
        try:
            if song_path is None:
                # For demo - using YouTube search
                self.log_message("🎵 Opening YouTube Music...", "info")
                webbrowser.open('https://www.youtube.com/results?search_query=lo+fi+music')
                self.speak_and_log("Opening YouTube Music. You can search for your favorite songs there.")
            else:
                if os.path.exists(song_path):
                    mixer.init()
                    mixer.music.load(song_path)
                    mixer.music.play()
                    self.log_message("🎵 Playing music...", "info")
                else:
                    self.log_message("❌ Music file not found", "error")
        except Exception as e:
            self.log_message(f"❌ Error playing music: {str(e)}", "error")
    
    # ============ FEATURE: WIKIPEDIA SEARCH ============
    def search_wikipedia(self, query):
        """Search Wikipedia"""
        try:
            self.log_message(f"🔍 Searching Wikipedia for: {query}", "info")
            results = wikipedia.summary(query, sentences=2)
            self.log_message(f"📚 Assistant: {results}", "assistant")
            self.engine.say(results)
            self.engine.runAndWait()
        except wikipedia.exceptions.PageError:
            self.speak_and_log("Sorry, page not found on Wikipedia.")
        except Exception as e:
            self.speak_and_log(f"Error searching Wikipedia: {str(e)}")
    
    # ============ PROCESS COMMANDS ============
    def process_command(self, command):
        """Process voice commands"""
        
        # Greeting
        if 'hello' in command or 'hi' in command:
            response = "Hello! How can I help you?"
            self.speak_and_log(response)
        
        elif 'how are you' in command:
            response = "I am doing great! Thanks for asking."
            self.speak_and_log(response)
        
        elif 'what is your name' in command:
            response = "I am your Advanced AI Voice Assistant, your digital helper."
            self.speak_and_log(response)
        
        # Time and Date
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            self.speak_and_log(response)
        
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {current_date}"
            self.speak_and_log(response)
        
        elif 'day' in command:
            day = datetime.datetime.now().strftime("%A")
            response = f"Today is {day}"
            self.speak_and_log(response)
        
        # Open Websites
        elif 'open google' in command:
            webbrowser.open('https://www.google.com')
            self.speak_and_log("Opening Google...")
        
        elif 'open youtube' in command:
            webbrowser.open('https://www.youtube.com')
            self.speak_and_log("Opening YouTube...")
        
        elif 'open facebook' in command:
            webbrowser.open('https://www.facebook.com')
            self.speak_and_log("Opening Facebook...")
        
        elif 'open github' in command:
            webbrowser.open('https://www.github.com')
            self.speak_and_log("Opening GitHub...")
        
        # Open Applications
        elif 'open notepad' in command:
            self.open_notepad()
        
        elif 'calculator' in command or 'open calculator' in command:
            self.open_calculator()
        
        # Jokes
        elif 'joke' in command or 'tell joke' in command:
            thread = threading.Thread(target=self.tell_joke)
            thread.daemon = True
            thread.start()
        
        # Weather
        elif 'weather' in command:
            # Extract city name
            city = "New Delhi"  # Default
            if 'in' in command:
                parts = command.split('in')
                if len(parts) > 1:
                    city = parts[-1].strip()
            thread = threading.Thread(target=lambda: self.get_weather(city))
            thread.daemon = True
            thread.start()
        
        # Play Music
        elif 'play music' in command or 'music' in command:
            thread = threading.Thread(target=self.play_music)
            thread.daemon = True
            thread.start()
        
        # Wikipedia Search
        elif 'wikipedia' in command or 'search' in command:
            query = command.replace('wikipedia', '').replace('search', '').strip()
            if query:
                thread = threading.Thread(target=lambda: self.search_wikipedia(query))
                thread.daemon = True
                thread.start()
            else:
                self.speak_and_log("What would you like me to search?")
        
        # Capabilities
        elif 'what can you do' in command or 'help' in command:
            response = """I can help you with:
- Telling you the time, date, and day
- Opening websites like Google, YouTube, Facebook, and GitHub
- Opening Notepad and Calculator
- Telling jokes
- Getting weather information for any city
- Playing music from YouTube
- Searching Wikipedia for information
- And much more! Try asking me anything."""
            self.speak_and_log(response)
        
        # Exit
        elif 'bye' in command or 'exit' in command or 'quit' in command:
            self.speak_and_log("Goodbye! Have a nice day!")
            self.root.after(1000, self.exit_app)
        
        # Default
        else:
            response = f"I'm not sure how to respond to that. You said: {command}."
            self.speak_and_log(response)


# ============ MAIN ============
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedVoiceAssistant(root)
    root.mainloop()
