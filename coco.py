import pvporcupine
import pyaudio
import struct
import pyttsx3
import speech_recognition as sr
import subprocess
import datetime
import webbrowser
import re
import sys
import os

# ADD THESE TWO CORRECT VALUES FROM PICOVOICE CONSOLE
ACCESS_KEY = "IB3Eut4N/RXw+mDjM4n1iRVsBz/jsh2grv4W64M9b85AjzrILMrnJg=="   
WAKEWORD_PATH = "hey-coco_windows.ppn"     
# Optional: Add fallback if file not found
if not os.path.exists(WAKEWORD_PATH):
    print(f"[ERROR] Wake word file not found: {WAKEWORD_PATH}")
    print("Download it from https://console.picovoice.ai/")
    exit()

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('voice', 'english')  # Optional: better voice

def speak(text):
    print("Coco:", text)
    engine.say(text)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=10, phrase_time_limit=10)
    try:
        query = r.recognize_google(audio, language='en-in').lower()
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        speak("I didn’t catch that. Please try again.")
        return ""
    except sr.RequestError:
        speak("No internet connection for speech recognition.")
        return ""
    except Exception as e:
        print("Listening error:", e)
        return ""

def execute_command(cmd):
    cmd = cmd.strip().lower()
    
    if 'open notepad' in cmd:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad")
    
    elif 'time' in cmd:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"It's {time}")
    
    elif 'date' in cmd:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {date}")
    
    elif 'shutdown' in cmd:
        speak("Shutting down in 10 seconds")
        os.system("shutdown /s /t 10")
    
    elif 'restart' in cmd:
        speak("Restarting...")
        os.system("shutdown /r /t 10")
    
    elif 'open google' in cmd:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    
    elif 'exit' in cmd or 'quit' in cmd or 'bye' in cmd:
        speak("Goodbye Sir!")
        return False
    
    else:
        speak("Sorry, I don't know that command yet.")
    
    return True

def wake_listener():
    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[WAKEWORD_PATH]
        )
    except Exception as e:
        print("Porcupine failed to start:", e)
        print("Check your AccessKey and .ppn file!")
        return

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    speak("Coco is now active. Say 'Hey Coco' to wake me up!")

    print("Listening for wake word... (Say: Hey Coco)")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected!")
                speak("Yes sir?")
                
                command = listen_command()
                if command:
                    if not execute_command(command):
                        break  # Exit on quit command
    except KeyboardInterrupt:
        speak("Goodbye!")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    wake_listener()