import speech_recognition as sr
import webbrowser
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

PHRASE_TIME_LIMIT = 5

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    print("Command:", command)

if __name__ == "__main__":
    speak("Initializing Micro")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Microphone ready...")

        while True:
            try:
                print("Listening for wake word...")
                audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)

                word = r.recognize_google(audio).lower()
                print("Heard:", word)

                if "jarvis" in word:
                    speak("Yes")

                    print("Listening for command...")
                    audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)

                    command = r.recognize_google(audio).lower()
                    processCommand(command)

            except Exception as e:
                print("Error:", e)