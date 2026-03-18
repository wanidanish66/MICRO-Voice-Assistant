import speech_recognition as sr     # This allows you to reference the speech_recognition library using the shorter name sr throughout your code
import webbrowser
import pyttsx3
import musicLibrary
import requests


recognizer = sr.Recognizer()        # recognizer class helps you to take speech recognition functionality
engine = pyttsx3.init()             # initilizing pyttsx
newsapi = "b258ed3179e8414f94df2743db0b0ef2"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
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

    # for news
    elif "open news" in c.lower():
        print("reading")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}") 
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    # for music library
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)


if __name__ == "__main__":
    speak("Intializing Micro......")
    while True:
        # listen for the wake word "Micro"
        # Use the default microphone as the audio source
        r = sr.Recognizer()
        
        
        print("recognizing....")
        # recognize speech using bing
        try:
            with sr.Microphone(device_index=2) as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)

            if "hello micro" in word.lower():
                speak("hello sir")

                # listen for command
                with sr.Microphone(device_index=2) as source:
                    print("Micro active....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("Error:", e)
