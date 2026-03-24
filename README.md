# MICRO-Voice-Assistant


🎤 MICRO - AI Voice Assistant

MICRO is a Python-based intelligent voice assistant that can listen, understand, and respond to user commands in real time. It integrates AI, speech recognition, and dynamic music playback to create a smart assistant experience.

🚀 Features
🎤 Wake word detection ("Hello Micro")
🧠 AI-powered responses
🎶 Play songs instantly (auto-play via YouTube)
🌐 Open popular websites (Google, YouTube, GitHub, etc.)
📰 Fetch and read latest news headlines
🔊 Natural voice responses using text-to-speech
🛠️ Tech Stack
Python
SpeechRecognition
pyttsx3 / edge-tts
pygame
yt-dlp
OpenAI API
Requests
📦 Installation
1. Clone the repository
git clone https://github.com/wanidanish66/MICRO-Voice-Assistant.git
cd micro-voice-assistant
2. Create virtual environment
python -m venv venv
3. Activate environment
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
▶️ Usage

Run the assistant:

python main.py

Say:

"Hello Micro"

Then give commands like:

"Play Kesariya"
"Open YouTube"
"Tell me the news"
"What is Artificial Intelligence?"
🎶 Music Playback

MICRO uses YouTube to:

Search songs dynamically
Play the most relevant result instantly

No need to store songs locally.

⚠️ Configuration

Update your API key in main.py:

api_key="YOUR_API_KEY_HERE"
📌 Future Improvements
⏯️ Music controls (pause, next, stop)
🖥️ GUI interface
🎧 In-app music player (no browser)
🤖 Offline wake word detection
🌍 Multi-language support
🤝 Contributing

Contributions are welcome! Feel free to fork this repo and submit a pull request.
