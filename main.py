import speech_recognition as sr     # Speech to text
import webbrowser                  # Open websites / links
import requests                    # API requests (news)
import asyncio                     # Async support
import edge_tts                    # Text-to-speech (AI voice)
import pygame                      # Audio playback
import time
import os
import random
from yt_dlp import YoutubeDL       # Fetch YouTube video links
from openai import OpenAI          # AI responses

# ---------------- RESPONSES ----------------
# this will reply randomly when wake word is detected
responses = [
    "Yes, I'm listening.",
    "How can I help you?",
    "What can I do for you?"
]

# Initialize recognizer and audio mixer
recognizer = sr.Recognizer()
pygame.mixer.init(frequency=22050, size=-16, channels=2)

# here use your own api to fetch news headlines
newsapi = "USE YOUR API"

# ---------------- SPEAK FUNCTION ----------------
# Convert text to speech using edge_tts and play it
async def speak_async(text):
    file = "voice.mp3"

    # Generates voice
    communicate = edge_tts.Communicate(
        text,
        voice="en-US-JennyNeural"
    )
    await communicate.save(file)

    # Play generated voice
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    # Wait until playback finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Cleanup
    pygame.mixer.music.unload()
    os.remove(file)

# Wrapper to run async speak function
def speak(text):
    asyncio.run(speak_async(text))
    time.sleep(0.3)  # Prevent mic from catching its own voice

# ---------------- YOUTUBE FUNCTION ----------------
# Get the best matching YouTube video link for a song
def get_youtube_link(song_name):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best'
    }

    with YoutubeDL(ydl_opts) as ydl:
        # Search YouTube and get first result
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        video = info['entries'][0]
        return video['webpage_url']

# ---------------- AI FUNCTION ----------------
# Send user command to AI model and return response
def aiProcess(command):
    try:
        client = OpenAI(
            api_key="YOUR_API_KEY_HERE",                     # visti NVIDIA to get API's  
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
# Handle all commands spoken by user
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

        # ---------- MUSIC (AUTO PLAY FROM YOUTUBE) ----------
        elif c.startswith("play"):
            try:
                # Clean command to extract song name
                song = c.replace("play", "").replace("song", "").replace("music", "").strip()

                if not song:
                    speak("Which song should I play?")
                    return

                speak(f"Playing {song}")

                # Get YouTube link and open it
                url = get_youtube_link(song)
                webbrowser.open(url)

            except Exception as e:
                print("Music Error:", e)
                speak("Couldn't find the song")

        # ---------- NEWS ----------
        elif "headlines" in c:
            speak("Fetching news...")

            # Fetch news from API
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}"
            )

            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

                if not articles:
                    speak("No news found.")
                    return

                # Speak top 5 headlines
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
            # Listen for wake word
            with sr.Microphone(device_index=2) as source:
                print("Listening for wake word...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            # Convert speech to text
            word = recognizer.recognize_google(audio)
            print("Wake word heard:", word)

            # Wake word detection (flexible)
            if "micro" in word.lower():
                speak(random.choice(responses))

                # Listen for actual command
                with sr.Microphone(device_index=2) as source:
                    print("Micro active...")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                print("Command:", command)

                # Process user command
                processCommand(command)

        except sr.WaitTimeoutError:
            # No speech detected within time
            pass

        except sr.UnknownValueError:
            # Speech not understood
            print("Could not understand")

        except Exception as e:
            print("Error:", e)