import speech_recognition as sr     # This allows you to reference the speech_recognition library using the shorter name sr throughout your code
import webbrowser
import pyttsx3

r = sr.Recognizer()        # recognizer class helps you to take speech recognition functionality
engine = pyttsx3.init()             # initilizing pyttsx

PHRASE_TIME_LIMIT = 5  # Set the phrase time limit in seconds
 
def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    print("Command:", command)


if __name__ == "__main__":
    speak("Intializing Micro......")
    while True:
        # listen for the wake word "Micro"
        # Use the default microphone as the audio source
    
        print("recognizing....")
        # recognize speech using bing
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening....")
                audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)

            word = r.recognize_google(audio).lower()
            print("Heard:", word)

            if "micro" in word:
                speak("Yes")
                # listen for command
                with sr.Microphone() as source:
                    print("Micro active....")
                    audio = r.listen(source, phrase_time_limit=PHRASE_TIME_LIMIT)

                command = r.recognize_google(audio)
                processCommand(command)

        except Exception as e:
            print("Error: ",e)
       
