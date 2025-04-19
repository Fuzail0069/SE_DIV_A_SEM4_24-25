import sqlite3
import requests
import pyttsx3
import threading
import speech_recognition as sr
import tkinter as tk
import webbrowser
import subprocess
import face_recognition
import cv2
import pickle
import datetime
import random
import os
import pyaudio
os.environ["PATH"] += os.pathsep + r"C:\Users\91932\Downloads\flac-1.5.0-win\flac-1.5.0-win\Win64"
import sys
vlc_path = r"C:\Users\Fuzail\Downloads\vlc-3.0.21-win64.exe"

os.add_dll_directory(vlc_path)
sys.path.append(vlc_path)
import vlc
import pywhatkit as kit
from pyowm import OWM
import os
import pywhatkit as kit
import random
import time
import pyautogui
from bs4 import BeautifulSoup
from textblob import TextBlob

# Initialize variables
is_listening = False
conversation_history = []

# Function to play a Bhajan from the playlist
def play_bhajan_from_playlist():
    playlist_url = "https://www.youtube.com/watch?v=-JYk923PASE&list=PLQe-3Jxts057a1SpuMBDZujWWoHGPqiMB&ab_channel=PujyaRajanJee"
    print(f"Playing Bhajan from the playlist: {playlist_url}")
    speak_response_local(f"Playing a Bhajan from the playlist now.", language_code="en")
    webbrowser.open(playlist_url)

# Initialize pyttsx3 engine for TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Set the rate (speed of speech)
engine.setProperty('rate', 150)

# Set the volume (0.0 to 1.0)
engine.setProperty('volume', 1)
recognizer = sr.Recognizer()
hotword = "sahayak"

video_path = "C:\\Users\\91932\\Videos\\Dell Mobile Connect\\Brahmastra Part One - Shiva 2022 V2 Hindi www.SSRmovies.Co 1080p HQ DVDScr x264 AAC.mkv"

# Initialize VLC media player
player = vlc.MediaPlayer(video_path)

# Create the Tkinter window
window = tk.Tk()
window.title("AI Assistant with Gemini Integration")
window.geometry("800x600")

# Create a canvas widget for the video
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Function to handle video restart
def video_ended(event):
    print("Video ended, restarting...")
    player.stop()
    player.play()

# Function to start the video and set up the loop
def start_video():
    player.set_fullscreen(True)
    media = vlc.Media(video_path)
    player.set_media(media)
    player.play()

# Farewell phrases to detect when the user says goodbye
farewell_phrases = ["bye", "goodbye", "see you", "good night", "take care", "farewell", "exit"]

# Function to execute system commands
def execute_system_command(command):
    try:
        if command == "shutdown":
            speak_response_local("Shutting down the system. Goodbye!")
            os.system("shutdown /s /t 1")
        elif command == "restart":
            speak_response_local("Restarting the system. Please wait...")
            os.system("shutdown /r /t 1")
        elif command == "sleep":
            speak_response_local("Putting the system to sleep...")
            subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        else:
            speak_response_local("Invalid command, nothing will happen.")
    except Exception as e:
        print(f"Error executing system command: {e}")

# Function to handle farewell and shutdown/restart/sleep prompt
def handle_farewell_and_shutdown(user_query):
    if any(farewell in user_query for farewell in farewell_phrases):
        speak_response_local("Goodbye! Do you want to shut down, restart, or sleep your PC? Please say one of these options.")
        user_response = recognize_speech()

        if user_response:
            if "shutdown" in user_response:
                execute_system_command("shutdown")
            elif "restart" in user_response:
                execute_system_command("restart")
            elif "sleep" in user_response:
                execute_system_command("sleep")
            else:
                speak_response_local("No action will be taken. Goodbye!")
        else:
            speak_response_local("I didn't catch that. Goodbye!")

# Function to set the language for Text-to-Speech
def set_language(language_code):
    voices = engine.getProperty('voices')
    for voice in voices:
        if language_code in voice.languages:
            engine.setProperty('voice', voice.id)
            break

# Function to speak a response using Text-to-Speech
def speak_response_local(text, language_code="en"):
    try:
        if text:
            print(f"Speaking: {text}")
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1)
            engine.say(text)
            engine.runAndWait()
        else:
            print("No response to speak.")
    except Exception as e:
        print(f"Error in TTS: {e}")

# Function to recognize speech
def recognize_speech(prompt=None, language='en-US'):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        if prompt:
            speak_response_local(prompt)
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=10)
            print("Processing the audio...")
            query = recognizer.recognize_google(audio, language=language)
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out, please try again.")
            return None

# Function to open applications

def open_application(app_name):
    app_name = app_name.lower()  # Normalize input to lowercase

    web_apps = {
        "chrome": "http://www.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "gmail": "https://mail.google.com"
    }

    if app_name in web_apps:
        webbrowser.open_new_tab(web_apps[app_name])

    elif app_name == "camera":
        open_camera_and_take_picture()  # Ensure this function is defined

    elif app_name == "youtube":
        speak_response_local("What do you want to search? Let me know and I will search it for you on YouTube.", language_code="en")
        search_query = recognize_speech()  # Get search query from user

        if search_query:
            youtube_search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            webbrowser.open_new_tab(youtube_search_url)  # Opens YouTube search results
        else:
            speak_response_local("Sorry, I didn't hear what you want to search for. Please try again.", language_code="en")

    else:
        speak_response_local(f"Sorry, I can't open {app_name} right now.", language_code="en")


# Function to open the camera and take a picture
def open_camera_and_take_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    print("Taking a picture...")
    ret, frame = cap.read()
    if ret:
        save_path = os.path.expanduser('~\\Pictures\\Saved Pictures')
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        filename = f"{save_path}\\picture_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        cv2.imwrite(filename, frame)
        speak_response_local(f"Picture taken and saved as {filename}", language_code="en")
        print(f"Picture saved as {filename}")
        webbrowser.open(f"file:///{filename}")
    cap.release()

# Function to compare the captured face with the database
def compare_faces_in_db(face_encoding):
    c.execute("SELECT name, face_encoding FROM users")
    rows = c.fetchall()

    for row in rows:
        stored_name = row[0]
        stored_face_encoding = pickle.loads(row[1])
        results = face_recognition.compare_faces([stored_face_encoding], face_encoding)
        if True in results:
            return stored_name
    return None

# Function to capture user face and check if it's an old user
def capture_user_face_and_name():
    global user_name
    global assistant_running

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    print("Please look at the camera...")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_locations:
            for face_encoding in face_encodings:
                matches = compare_faces_in_db(face_encoding)
                if matches:
                    name = matches
                    print(f"Welcome back, {name}!")
                    speak_response_local(f"Welcome back, {name}!", language_code="en")
                    speak_response_local("How can I help you?", language_code="en")
                    cap.release()
                    cv2.destroyAllWindows()
                    assistant_running = True
                    return
                else:
                    print("This is a new user. What's your name?")
                    speak_response_local("This is a new user. What's your name?", language_code="en")
                    user_name = recognize_speech()
                    if user_name:
                        store_user_face_and_name(face_encoding, user_name)
                        print(f"Face captured and saved for {user_name}")
                        speak_response_local(f"Face captured and saved for {user_name}", language_code="en")
                        speak_response_local(f"Hi, {user_name}. How can I help you?", language_code="en")
                    cap.release()
                    cv2.destroyAllWindows()
                    assistant_running = True
                    return

        cv2.imshow("Capturing Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to store the user's face and name in the database
def store_user_face_and_name(face_encoding, user_name):
    encoded_face = pickle.dumps(face_encoding)
    c.execute("INSERT INTO users (name, face_encoding) VALUES (?, ?)", (user_name, encoded_face))
    conn.commit()
    print(f"User {user_name} with face encoding saved to database.")

# Function to send a WhatsApp message
def send_whatsapp_message(contact, message):
    kit.sendwhatmsg(+918652544398, "hi", datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
    time.sleep(10)
    pyautogui.write(message)
    pyautogui.press('enter')
    print(f"Message sent to {contact}: {message}")

# Function to get weather information
def get_weather_info(city):
    owm = OWM('f0083fab4415debaa787ca870f26552f')  # Replace with your OWM API key
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    temperature = weather.temperature('celsius')['temp']
    status = weather.detailed_status
    return f"The current temperature in {city} is {temperature}°C with {status}."

# Function to play music
def play_music():
    player = vlc.MediaPlayer("path_to_music.mp3")  # Replace with actual music file path
    player.play()
    speak_response_local("Playing music now.", language_code="en")

# Function to query Gemini API for a response
def get_gemini_response(user_query):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCP6-LRx8ScFASQ1_qVDemDWB-8imjl3B8"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "parts": [{"text": user_query}]
            }
        ]
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print("API Response:", response_data)

        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            candidate = response_data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                text_part = candidate['content']['parts'][0]['text']
                return text_part
            else:
                return "Sorry, I couldn't find any parts in the response."
        else:
            return "Sorry, I encountered an issue with the response format."
    
    except requests.exceptions.RequestException as e:
        print(f"Error while querying Gemini API: {e}")
        return "Sorry, I encountered an error while fetching the response."

    except ValueError as e:
        print(f"Error while parsing the response: {e}")
        return "Sorry, I encountered an error while processing the response."

# Function to process user commands
def update_response_text(text):
    response_text.insert(tk.END, text + '\n')
    response_text.see(tk.END)  # Scroll to the bottom

def process_user_commands():
    global assistant_running, response_text
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")

    while assistant_running:
        user_query = recognize_speech()

        if user_query:
            # Add the user query to the conversation history
            conversation_history.append(user_query)

            # Perform sentiment analysis
            sentiment = TextBlob(user_query).sentiment
            if sentiment.polarity > 0:
                mood = "positive"
            elif sentiment.polarity < 0:
                mood = "negative"
            else:
                mood = "neutral"

            # Predefined commands (with corresponding actions)
            if "play bhajan" in user_query:  # Contextual response
                if mood == "negative":
                    speak_response_local("I understand you might be feeling down. Let's play a Bhajan to lift your spirits.", language_code="en")
                else:
                    speak_response_local("Sure, I can play a Bhajan for you.", language_code="en")
                play_bhajan_from_playlist()

            # Handle farewell and shutdown commands
            handle_farewell_and_shutdown(user_query)

            if "clear the database" in user_query:
                clear_database()

            # Check for Farewell Commands
            if any(farewell in user_query for farewell in farewell_phrases):
                farewell_response = "Goodbye! Have a great day ahead!"
                speak_response_local(farewell_response)
                print(farewell_response)
                assistant_running = False
                window.quit()
                window.destroy()
                break

            # Check if the query matches predefined commands (open applications)
            elif "open" in user_query:
                if "chrome" in user_query:
                    open_application("chrome")
                elif "whatsapp" in user_query:
                    open_application("whatsapp")
                elif "gmail" in user_query:
                    open_application("gmail")
                elif "camera" in user_query:
                    open_application("camera")
                elif "youtube" in user_query:
                    speak_response_local("What do you want to search? Let me know and I will search it for you on YouTube.", language_code="en")
                    search_query = recognize_speech()  # Ask the user what to search
                    if search_query:
                        search_and_play_video(search_query)  # Search and play a video
                    else:
                        speak_response_local("Sorry, I didn't hear what you want to search for. Please try again.", language_code="en")
                else:
                    speak_response_local("I am unable to open that application.")
                
            # Other predefined functionalities
            elif "weather" in user_query:
                response = get_weather_info('MUMBAI')  # Example city
                window.after(0, update_response_text, response)
                speak_response_local(response)
            elif "music" in user_query:
                play_music()
            elif "message" in user_query:
                contact = "Fuzail"  # Example contact name
                message = "Hello from fuzail assistant!"  # Example message
                send_whatsapp_message(contact, message)
            elif "stop" in user_query:
                assistant_running = False
                speak_response_local("Assistant has stopped.", language_code="en")
                break

            # If the query does not match any predefined commands, query the Gemini API
            else:
                gemini_response = get_gemini_response(user_query)
                window.after(0, update_response_text, gemini_response)
                speak_response_local(gemini_response)

        time.sleep(1)  # Small delay to prevent high CPU usage in the loop

# Function to start assistant automatically
def start_assistant():
    print("Assistant started. Listening for the hotword 'Sahayak'.")
    threading.Thread(target=listen_for_hotword, daemon=True).start()
    global assistant_running
    assistant_running = True

    # Greet and ask for name if it's the first time
    speak_response_local("Hi, I'm your Sahayak, how can I help you?", language_code="en")
    
    # Capture face and name
    capture_user_face_and_name()
    
    # Process user commands
    threading.Thread(target=process_user_commands, daemon=True).start()

# Function to listen for the hotword
def listen_for_hotword():
    global is_listening
    hotword = "sahayak"

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for hotword...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                user_input = recognizer.recognize_google(audio).lower()

                if hotword in user_input:
                    if not is_listening:
                        is_listening = True
                        print(f"Hotword detected: {hotword}!")
                        speak_response_local("I'm listening to your command.")
                        process_user_commands()
                        is_listening = False

                time.sleep(1)

            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
                break
# Predefined commands
predefined_commands = {
    "stop": "Stopping the process...",
    "status": "System is running smoothly.",
    "help": "Available commands: stop, status, help"
}

def handle_input(user_input):
    # Check if it's a predefined command
    if user_input.lower() in predefined_commands:
        response = predefined_commands[user_input.lower()]
        
        # Stop command: Exit the program or stop further processing
        if user_input.lower() == "stop":
            print(response)
            exit()  # Stops the program immediately
        
        return response
    
    # Otherwise, send it to Gemini API
    response = send_to_gemini_api(user_input)
    return response

# Initialize the SQLite Database to store user info
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, face_encoding BLOB, voice_encoding BLOB)''')
conn.commit()

# Run the assistant as soon as the program starts
start_assistant()
player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, video_ended)
start_video()
window.mainloop()