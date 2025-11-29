 ### Jarvis Desktop Voice Assistant

A personal desktop voice assistant inspired by Iron Man’s Jarvis. It listens for a wake word, processes voice commands, and performs tasks like opening apps, searching the web, telling the time, and more.

Features

• Wake word detection using Porcupine
• Speech recognition
• Text to speech responses
• System automation like opening apps and websites
• Custom commands
• Modular structure for easy updates
• Cross-platform Python support
• Future support planned for GUI (Jarvis-style HUD)

Tech Stack

• Python
• Porcupine (Wake word engine)
• SpeechRecognition
• Pyttsx3 or any TTS engine
• Qt for optional GUI
• Custom command modules

Installation

Clone the project

git clone https://github.com/thevidyasagar/Assistant-jarvis
cd jarvis-assistant


Create a virtual environment

python -m venv .venv
source .venv/Scripts/activate


Install dependencies

pip install -r requirements.txt


Add your Porcupine keyword file (.ppn)
Place it inside:

core/wake_engine/


Run the assistant

python main.py

How It Works

Porcupine listens for the wake word.

Once triggered, the STT engine converts your speech to text.

The command handler checks what you said and matches it with defined actions.

The TTS engine replies with a natural voice.

Supported Commands

Examples you can include:
• “Open YouTube”
• “Search for JavaScript tutorials”
• “What’s the time”
• “Play music”
• “Shutdown the system”
You can add more commands by editing command_handler.py.

Adding New Commands

Inside command_handler.py, add a new function and map it to a keyword. For example:

if "calculator" in command:
    open_calculator()

Troubleshooting

• If Porcupine throws a keyword error, check your .ppn file platform.
• If microphone is not detected, check audio input settings.
• Windows DPI warning from Qt can be ignored or fixed using qt.conf.

Future Scope

• Full Jarvis-style animated UI
• Wake word customization
• Offline mode
• Integration with home automation
• Real-time system monitoring widgets

License

MIT License
