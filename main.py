import speech_recognition as sr     
import webbrowser
import musicLibrary
import requests
import asyncio
import edge_tts
import pygame
import time
import os
import random

responses = [
    "Yes, I'm listening.",
    "How can I help you?",
    "What can I do for you?"
]


recognizer = sr.Recognizer()        
pygame.mixer.init(frequency=22050, size=-16, channels=2)

newsapi = "b258ed3179e8414f94df2743db0b0ef2"     # api key for news

# -----------------------------speak functionality for micro-----------------------------

async def speak_async(text):
    file = "voice.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice="en-US-JennyNeural"
    )
    await communicate.save(file)

    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(file)

def speak(text):
    asyncio.run(speak_async(text))


def processCommand(c):
    #---------------------------------for opening various applications--------------------- 

    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")

    elif "open linkdin" in c.lower():
        webbrowser.open("https://linkdin.com")

    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
        
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    # -----------------------------for music library----------------------------
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    #----------------------------- for news command -------------------------------

    elif "news" in c.lower():
        print("Fetching news...")
    r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
    
    print("Status Code:", r.status_code)

    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])

        if not articles:
            speak("No news found.")
            return

        for article in articles[:5]:  # limit to 5
            print(article['title'])
            speak(article['title'])
    else:
        speak("Failed to fetch news")


#------------------------------this is main content---------------------------------

if __name__ == "__main__":
    speak("Intializing Micro......")
    while True:
        r = sr.Recognizer()
        
        
        print("recognizing....")

        try:
            with sr.Microphone(device_index=2) as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)

            if "hello micro" in word.lower():
                speak(random.choice(responses))


                # listen for command
                with sr.Microphone(device_index=2) as source:
                    print("Micro active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("Error:", e)
