# core/tts.py — Stable async TTS using edge-tts + pydub
import asyncio
import edge_tts
import threading
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

VOICE = "en-US-AriaNeural"

async def _speak_async(text):
    try:
        # Create temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        path = tmp.name

        # Create TTS audio
        tts = edge_tts.Communicate(text, VOICE)
        await tts.save(path)

        # Play audio
        audio = AudioSegment.from_file(path, format="mp3")
        play(audio)

        os.remove(path)

    except Exception as e:
        print("TTS Error:", e)


def speak(text: str):
    """Non-blocking TTS"""
    threading.Thread(target=lambda: asyncio.run(_speak_async(text))).start()
