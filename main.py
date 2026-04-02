import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
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

responses = [
    "Yes, I'm listening.",
    "How can I help you?",
    "What can I do for you?"
]

recognizer = sr.Recognizer()
pygame.mixer.init(frequency=22050, size=-16, channels=2)

newsapi = "YOUR-NEWSAPI-KEY-HERE"

listening_active = False
listener_thread = None


async def speak_async(text):
    file = "voice.mp3"
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save(file)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove(file)


def speak(text):
    asyncio.run(speak_async(text))
    time.sleep(0.3)


def get_youtube_link(song_name):
    ydl_opts = {"quiet": True, "format": "bestaudio/best"}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        video = info["entries"][0]
        return video["webpage_url"]


def aiProcess(command):
    try:
        client = OpenAI(
            api_key="YOUR-OPENAI-KEY-HERE",
            base_url="https://integrate.api.nvidia.com/v1",
        )
        completion = client.chat.completions.create(
            model="deepseek-ai/deepseek-v3.1-terminus",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Micro."},
                {"role": "user", "content": command},
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI error: {e}"


def processCommand(c, log_func, set_status):
    c = c.lower()
    try:
        if "open google" in c:
            webbrowser.open("https://google.com")
            log_func("Micro: Opening Google...")
        elif "open facebook" in c:
            webbrowser.open("https://facebook.com")
            log_func("Micro: Opening Facebook...")
        elif "open instagram" in c:
            webbrowser.open("https://instagram.com")
            log_func("Micro: Opening Instagram...")
        elif "open linkedin" in c:
            webbrowser.open("https://linkedin.com")
            log_func("Micro: Opening LinkedIn...")
        elif "open github" in c:
            webbrowser.open("https://github.com")
            log_func("Micro: Opening GitHub...")
        elif "open youtube" in c:
            webbrowser.open("https://youtube.com")
            log_func("Micro: Opening YouTube...")
        elif c.startswith("play"):
            song = c.replace("play", "").replace("song", "").replace("music", "").strip()
            if not song:
                speak("Which song should I play?")
                log_func("Micro: Which song should I play?")
                return
            speak(f"Playing {song}")
            log_func(f"Micro: Playing {song}")
            url = get_youtube_link(song)
            webbrowser.open(url)
        elif "headlines" in c:
            speak("Fetching news...")
            log_func("Micro: Fetching news...")
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}"
            )
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if not articles:
                    speak("No news found.")
                    log_func("Micro: No news found.")
                    return
                for article in articles[:5]:
                    log_func(f"News: {article['title']}")
                    speak(article["title"])
            else:
                speak("Failed to fetch news")
                log_func("Micro: Failed to fetch news.")
        else:
            speak("Thinking...")
            log_func("Micro: Thinking...")
            set_status("Thinking...", "#f39c12")
            output = aiProcess(c)
            log_func(f"Micro: {output}")
            speak(output)
    except Exception as e:
        log_func(f"Error: {e}")
        speak("Something went wrong")


def listen_loop(log_func, set_status, is_active):
    speak("Initializing Micro")
    log_func("Micro: Initializing...")

    while is_active():
        try:
            set_status("Listening for wake word...", "#3498db")
            with sr.Microphone(device_index=2) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            word = recognizer.recognize_google(audio)
            log_func(f"Heard: {word}")

            if "micro" in word.lower():
                speak(random.choice(responses))
                log_func("Micro: Activated! Listening for command...")
                set_status("Activated — speak your command!", "#2ecc71")

                with sr.Microphone(device_index=2) as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                command = recognizer.recognize_google(audio)
                log_func(f"You: {command}")
                set_status("Processing...", "#9b59b6")
                processCommand(command, log_func, set_status)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            log_func("Could not understand audio.")
        except Exception as e:
            if is_active():
                log_func(f"Error: {e}")

    set_status("Stopped", "#e74c3c")


class MicroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Micro — Voice Assistant")
        self.root.geometry("640x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.is_running = False

        self._build_ui()

    def _build_ui(self):
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(pady=(20, 5))

        tk.Label(
            title_frame,
            text="MICRO",
            font=("Segoe UI", 32, "bold"),
            fg="#e94560",
            bg="#1a1a2e",
        ).pack()

        tk.Label(
            title_frame,
            text="Voice Assistant",
            font=("Segoe UI", 12),
            fg="#a0a0b0",
            bg="#1a1a2e",
        ).pack()

        status_frame = tk.Frame(self.root, bg="#16213e", padx=20, pady=10)
        status_frame.pack(fill="x", padx=30, pady=(10, 5))

        tk.Label(
            status_frame,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            fg="#a0a0b0",
            bg="#16213e",
        ).pack(side="left")

        self.status_label = tk.Label(
            status_frame,
            text="Idle",
            font=("Segoe UI", 10, "bold"),
            fg="#e74c3c",
            bg="#16213e",
        )
        self.status_label.pack(side="left", padx=8)

        self.indicator = tk.Canvas(
            status_frame, width=14, height=14, bg="#16213e", highlightthickness=0
        )
        self.indicator.pack(side="right")
        self.dot = self.indicator.create_oval(2, 2, 12, 12, fill="#e74c3c", outline="")

        log_frame = tk.Frame(self.root, bg="#1a1a2e")
        log_frame.pack(fill="both", expand=True, padx=30, pady=5)

        tk.Label(
            log_frame,
            text="Activity Log",
            font=("Segoe UI", 10, "bold"),
            fg="#a0a0b0",
            bg="#1a1a2e",
        ).pack(anchor="w")

        self.log_box = scrolledtext.ScrolledText(
            log_frame,
            state="disabled",
            height=14,
            font=("Consolas", 10),
            bg="#0f3460",
            fg="#e0e0f0",
            insertbackground="white",
            relief="flat",
            borderwidth=0,
            wrap="word",
        )
        self.log_box.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.root, bg="#1a1a2e")
        btn_frame.pack(pady=(10, 20))

        self.toggle_btn = tk.Button(
            btn_frame,
            text="  START MICRO  ",
            font=("Segoe UI", 12, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#c73652",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.toggle_listening,
        )
        self.toggle_btn.pack(side="left", padx=10)

        clear_btn = tk.Button(
            btn_frame,
            text="  CLEAR LOG  ",
            font=("Segoe UI", 12, "bold"),
            bg="#2c2c54",
            fg="#a0a0b0",
            activebackground="#3d3d70",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.clear_log,
        )
        clear_btn.pack(side="left", padx=10)

    def log(self, message):
        def _log():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"{message}\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

        self.root.after(0, _log)

    def set_status(self, text, color):
        def _update():
            self.status_label.configure(text=text, fg=color)
            self.indicator.itemconfig(self.dot, fill=color)

        self.root.after(0, _update)

    def toggle_listening(self):
        global listening_active, listener_thread

        if not self.is_running:
            self.is_running = True
            listening_active = True
            self.toggle_btn.configure(text="  STOP MICRO  ", bg="#27ae60", activebackground="#1e8449")
            self.set_status("Starting...", "#f39c12")
            listener_thread = threading.Thread(
                target=listen_loop,
                args=(self.log, self.set_status, lambda: listening_active),
                daemon=True,
            )
            listener_thread.start()
        else:
            listening_active = False
            self.is_running = False
            self.toggle_btn.configure(text="  START MICRO  ", bg="#e94560", activebackground="#c73652")
            self.set_status("Stopped", "#e74c3c")
            self.log("Micro: Stopped.")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def on_close(self):
        global listening_active
        listening_active = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MicroGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
