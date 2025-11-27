# import speech_recognition as sr
# import pyttsx3
# import datetime
# import wikipedia
# import webbrowser
# import os
# import pyjokes
# import pywhatkit  # for YouTube playback

# # Initialize text-to-speech engine
# engine = pyttsx3.init('sapi5')  # Windows uses sapi5, works on Linux/Mac too with tweaks
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female (if available)
# engine.setProperty('rate', 180)  # speaking speed

# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()

# def wish_me():
#     hour = datetime.datetime.now().hour
#     if 0 <= hour < 12:
#         speak("Good Morning!")
#     elif 12 <= hour < 18:
#         speak("Good Afternoon!")
#     else:
#         speak("Good Evening!")
#     speak("I am your voice assistant. How can I help you today?")

# def take_command():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         r.energy_threshold = 400
#         audio = r.listen(source)

#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"You said: {query}\n")
#     except Exception as e:
#         print("Say that again please...")
#         return "None"
#     return query.lower()

# if __name__ == "__main__":
#     wish_me()
#     while True:
#         query = take_command()

#         # Logic for executing tasks
#         if 'wikipedia' in query:
#             speak('Searching Wikipedia...')
#             query = query.replace("wikipedia", "")
#             result = wikipedia.summary(query, sentences=2)
#             speak("According to Wikipedia")
#             print(result)
#             speak(result)

#         elif 'open youtube' in query:
#             webbrowser.open("https://youtube.com")

#         elif 'open google' in query:
#             webbrowser.open("https://google.com")

#         elif 'open stack overflow' in query:
#             webbrowser.open("https://stackoverflow.com")

#         elif 'play' in query:
#             song = query.replace('play', '')
#             speak(f'Playing {song}')
#             pywhatkit.playonyt(song)

#         elif 'time' in query:
#             str_time = datetime.datetime.now().strftime("%H:%M")
#             speak(f"The time is {str_time}")

#         elif 'date' in query:
#             str_date = datetime.datetime.now().strftime("%B %d, %Y")
#             speak(f"Today's date is {str_date}")

#         elif 'open vs code' in query or 'open code' in query:
#             code_path = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  # CHANGE THIS PATH
#             os.startfile(code_path)

#         elif 'joke' in query:
#             joke = pyjokes.get_joke()
#             print(joke)
#             speak(joke)

#         elif 'shutdown' in query or 'shut down' in query:
#             speak("Shutting down the computer")
#             os.system("shutdown /s /t 5")

#         elif 'restart' in query:
#             speak("Restarting the computer")
#             os.system("shutdown /r /t 5")

#         elif 'sleep' in query:
#             speak("Putting computer to sleep")
#             os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

#         elif 'exit' in query or 'quit' in query or 'bye' in query:
#             speak("Goodbye! Have a great day!")
#             break



from youtubesearchpython import VideosSearch

def play_song(song_name):
    search = VideosSearch(song_name, limit=1)
    url = search.result()['result'][0]['link']
    webbrowser.open(url)
    speak(f"Playing {song_name}")

# Use in your assistant
elif 'play' in query:
    song = query.replace('play', '').strip()
    speak(f"Playing {song} on YouTube")
    play_song(song)