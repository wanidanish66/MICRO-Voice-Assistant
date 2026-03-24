import speech_recognition as sr
import webbrowser
import requests
import asyncio
import edge_tts
import pygame
import time
import os
import random
from yt_dlp import YoutubeDL
from openai import OpenAI

# ---------------- RESPONSES ----------------
responses = [
    "Yes, I'm listening.",
    "How can I help you?",
    "What can I do for you?"
]

recognizer = sr.Recognizer()
pygame.mixer.init(frequency=22050, size=-16, channels=2)

newsapi = "b258ed3179e8414f94df2743db0b0ef2"

# ---------------- SPEAK FUNCTION ----------------
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
    time.sleep(0.3)  # small delay to avoid mic conflict

# ---------------- YOUTUBE FUNCTION ----------------
def get_youtube_link(song_name):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        video = info['entries'][0]
        return video['webpage_url']

# ---------------- AI FUNCTION ----------------
def aiProcess(command):
    try:
        client = OpenAI(
            api_key="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",
            base_url="https://integrate.api.nvidia.com/v1"
        )

        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-v3.1-terminus",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Micro."},
                {"role": "user", "content": command}
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"AI error: {e}"

# ---------------- COMMAND PROCESSOR ----------------
def processCommand(c):
    c = c.lower()

    try:
        # ---------- OPEN WEBSITES ----------
        if "open google" in c:
            webbrowser.open("https://google.com")

        elif "open facebook" in c:
            webbrowser.open("https://facebook.com")

        elif "open instagram" in c:
            webbrowser.open("https://instagram.com")

        elif "open linkedin" in c:
            webbrowser.open("https://linkedin.com")

        elif "open github" in c:
            webbrowser.open("https://github.com")

        elif "open youtube" in c:
            webbrowser.open("https://youtube.com")

        # ---------- MUSIC (AUTO PLAY) ----------
        elif c.startswith("play"):
            try:
                song = c.replace("play", "").replace("song", "").replace("music", "").strip()

                if not song:
                    speak("Which song should I play?")
                    return

                speak(f"Playing {song}")

                url = get_youtube_link(song)
                webbrowser.open(url)

            except Exception as e:
                print("Music Error:", e)
                speak("Couldn't find the song")

        # ---------- NEWS ----------
        elif "headlines" in c:
            speak("Fetching news...")

            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}"
            )

            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if not articles:
                    speak("No news found.")
                    return

                for article in articles[:5]:
                    print(article['title'])
                    speak(article['title'])
            else:
                speak("Failed to fetch news")

        # ---------- AI FALLBACK ----------
        else:
            speak("Thinking...")
            output = aiProcess(c)
            print("AI:", output)
            speak(output)

    except Exception as e:
        print("Command Error:", e)
        speak("Something went wrong")

# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":
    speak("Initializing Micro")

    while True:
        try:
            with sr.Microphone(device_index=2) as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            print("Wake word heard:", word)

            # More flexible wake detection
            if "micro" in word.lower():
                speak(random.choice(responses))

                with sr.Microphone(device_index=2) as source:
                    print("Micro active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                processCommand(command)

        except sr.WaitTimeoutError:
            pass

        except sr.UnknownValueError:
            print("Could not understand")

        except Exception as e:
            print("Error:", e)