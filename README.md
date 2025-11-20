📌 Jarvis Assistant – AI Powered Desktop Voice Assistant

Jarvis Assistant एक Python-based desktop voice assistant है।
ये wake-word detection, speech-to-text, text-to-speech, LLM-based intent handling और HUD UI जैसे features को support करता है।

🚀 Features
✔ Wake-Word Detection

Porcupine का उपयोग करके “Jarvis” या custom wake-word सुनकर auto-activate होता है।

✔ Speech-to-Text

Recorded audio को OpenAI Whisper या अन्य STT models से process करता है।

✔ Text-to-Speech

Edge-TTS या किसी भी TTS model से natural voice output देता है।

✔ AI Brain

Core LLM (Groq / OpenAI / Custom model) को use करके intelligent responses और task execution करता है।

✔ RAG Support

Local files से context पढ़कर answer improve करता है।

✔ HUD UI

On-screen floating UI जो mic status और responses show करती है।

✔ Console UI

Debug mode के लिए lightweight terminal interface।

📂 Project Structure
jarvis assistant/
│
├── main.py                 # Entry point (wake-word + pipeline)
│
├── core/                   # AI brain, tools, memory, STT, TTS
├── rag/                    # RAG engine + file readers
├── ui/                     # HUD + Console
├── agent/                  # Memory and tool engine
├── audio/                  # Input/Output samples
├── config/                 # Settings (API keys via .env)
│
├── requirements.txt        # Dependencies
└── README.md               # Project documentation

🔧 Installation
1. Clone the repository
git clone https://github.com/thevidyasagar/Assistant-jarvis.git
cd Assistant-jarvis

2. Create virtual environment
python -m venv .venv

3. Activate

Windows:

.venv\Scripts\activate

4. Install dependencies
pip install -r requirements.txt

🔑 Environment Variables (Required)

Create a file:

config/.env


Add inside:

OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here


⚠ यह फाइल GitHub पर push नहीं होनी चाहिए।
यह .gitignore में already included है।

▶️ Running Jarvis
python main.py

🧠 How It Works

Wake-word listener audio capture शुरू करता है

Wake word मिलने पर STT engine text generate करता है

Core LLM query process करता है और plan बनाता है

Tools + memory engine tasks execute करते हैं

Output voice TTS के द्वारा बोलकर सुनाया जाता है

HUD पर status दिखाया जाता है

🛠 Technologies Used

Python 3.10

Porcupine Wake-Word

Whisper STT

Edge-TTS

Groq / OpenAI LLM

PyQt6 for HUD UI

RAG Engine

JSON Memory

🤝 Contributing

Pull requests welcome हैं।
Large features पहले issue में discuss करें।

📜 License

MIT License.
