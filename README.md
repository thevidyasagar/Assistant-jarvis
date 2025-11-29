Jarvis Desktop Voice Assistant

A clean and modular Python voice assistant inspired by Jarvis.
It listens for a wake word, understands your command, and performs tasks on your system.

🎨 Project Preview
📌 Features
• Wake Word Activation

Listens continuously until the wake word is spoken.

• Speech Recognition

Understands commands using STT.

• Natural Voice Replies

Responds using a built-in TTS engine.

• App and Website Automation

Open apps, run system tools, search the web.

• Modular Command System

Add new skills easily by editing one file.

• Optional Futuristic GUI

A Jarvis-style animated UI (under development).

🛠️ Tech Stack
Component	Used
Voice Wake Engine	Porcupine
Speech to Text	SpeechRecognition
Text to Speech	Pyttsx3
Audio Input	PyAudio
UI (optional)	PyQt
Language	Python

🚀 Installation Guide
1. Clone Repository
git clone https://github.com/thevidyasagar/Assistant-jarvis
cd jarvis-assistant

2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Add Your Wake Word File (.ppn)

Place it in:

core/wake_engine/

5. Run Jarvis
python main.py

⚙️ How Jarvis Works
1. Wake Word Engine Listens

Jarvis wakes up when you say the trigger phrase.

2. Speech Recognition

Your command is converted into text.

3. Command Handler

The system checks what action matches the command.

4. Response + Action

Jarvis replies and performs the task.

🎤 Supported Commands
System Commands

“Open Chrome”

“Open Notepad”

“Shutdown system”

Information

“What’s the time”

“What’s the date today”

Search

“Search Python tutorials”

“Search weather in Delhi”

Media

“Play music”

➕ Add Your Own Commands

Open: core/command_handler.py

Example:

if "calculator" in command:
    os.system("calc.exe")


You can create unlimited commands.

🔧 Troubleshooting
Wake Word Not Working

Check if your .ppn matches Windows.

Microphone Errors

Set default input device in Windows sound settings.

DPI Warning from Qt

Safe to ignore. Can be fixed using qt.conf.

🚧 Future Updates

Animated Jarvis HUD UI

System monitoring widgets

Custom wake words

Offline mode

Home automation support

📄 License

MIT License
