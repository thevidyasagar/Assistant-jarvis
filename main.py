# main.py — Final Clean + Stable Jarvis

import os
import sys
import time
import tempfile
import threading
import numpy as np
import sounddevice as sd
import wavio

from core.wake_porcupine import PorcupineListener
from core.stt import transcribe_file
from core.tts import speak
from core.brain import handle_user_text

from ui.hud import JarvisHUD
from ui.console import JarvisConsole

from PyQt6.QtGui import QKeySequence, QIcon, QShortcut, QAction
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu


# ---------- MIC & AUDIO SETTINGS ----------
MIC_DEVICE = 9
SAMPLE_RATE = 48000         # FIXED FOR WASAPI
RECORD_SECONDS = 2
WAKE_SENS = 0.90
continuous_mode = False


# ---------- RECORD AUDIO WITH RMS ----------
def record_audio_rms(path, duration, hud):
    def callback(indata, frames, t, status):
        try:
            mono = indata.mean(axis=1)
            rms = float(np.sqrt((mono ** 2).mean()))
            level = min(1.0, rms * 18)
            hud.set_voice_level(level)
        except:
            pass

    with sd.InputStream(
        device=MIC_DEVICE,
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=callback
    ):
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            device=MIC_DEVICE
        )
        sd.wait()
        wavio.write(path, audio, SAMPLE_RATE, sampwidth=2)

    hud.set_voice_level(0.0)


# ---------- VOICE CONFIRMATION ----------
def ask_confirmation_via_voice(prompt_text, hud, timeout=3):
    speak(prompt_text)
    hud.show_listening()
    hud.play_sound("wake")

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()

    try:
        audio = sd.rec(
            int(timeout * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            device=MIC_DEVICE
        )
        sd.wait()
        wavio.write(tmp.name, audio, SAMPLE_RATE, sampwidth=2)

        text = transcribe_file(tmp.name).lower()
        print("Confirm:", text)

        yes_words = ["yes", "haan", "ha", "ok", "sure"]
        no_words = ["no", "nahi", "mat"]

        if any(y in text for y in yes_words): return True
        if any(n in text for n in no_words): return False

    except Exception as e:
        print("confirm error:", e)

    finally:
        try:
            os.remove(tmp.name)
        except:
            pass

    return False


# ---------- HANDLE ONE COMMAND ----------
def handle_one_command(hud):
    hud.fade_in()
    hud.show_listening()
    hud.play_sound("wake")

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()

    try:
        record_audio_rms(tmp.name, RECORD_SECONDS, hud)

        hud.show_thinking()
        hud.play_sound("think")

        text = transcribe_file(tmp.name)
        print("User:", text)

        if not text.strip():
            hud.show_speaking("Samajh nahi aaya.")
            speak("Samajh nahi aaya, phir se bolo.")
            return

        response = handle_user_text(
            text,
            ask_confirm_fn=lambda p: ask_confirmation_via_voice(p, hud)
        )

        if response.get("status") == "cancelled":
            hud.show_speaking("Cancel kar diya.")
            speak("Cancel kar diya.")
            return

        for item in response.get("results", []):
            if item.get("type") == "chat":
                reply = item.get("reply", "")
                hud.show_speaking(reply)
                hud.play_sound("done")
                speak(reply)

            elif item.get("type") == "tool":
                out = str(item.get("result", "Done"))
                hud.show_speaking(out)
                hud.play_sound("done")
                speak(out)

    except Exception as e:
        print("Command error:", e)

    finally:
        hud.show_ready()
        hud.fade_out()
        try:
            os.remove(tmp.name)
        except:
            pass


# ---------- MAIN LOOP ----------
def run_loop():
    print("Starting Jarvis...")

    hud = JarvisHUD(size=380)
    hud.start(blocking=False)
    hud.show_ready()

    console = JarvisConsole()

    def console_cmd(text):
        res = handle_user_text(text)
        for item in res.get("results", []):
            if item.get("type") == "chat":
                return item["reply"]
        return "Done"

    console.on_command = console_cmd

    QShortcut(QKeySequence("Alt+J"), hud._w).activated.connect(lambda: console.show())

    try:
        app = QApplication.instance()
        icon = QIcon()
        tray = QSystemTrayIcon(icon, app)

        menu = QMenu()
        show_act = QAction("Show HUD")
        hide_act = QAction("Hide HUD")
        quit_act = QAction("Quit")

        show_act.triggered.connect(lambda: hud._w.show())
        hide_act.triggered.connect(lambda: hud._w.hide())
        quit_act.triggered.connect(lambda: (hud.stop(), sys.exit(0)))

        menu.addAction(show_act)
        menu.addAction(hide_act)
        menu.addSeparator()
        menu.addAction(quit_act)

        tray.setContextMenu(menu)
        tray.show()

    except Exception as e:
        print("Tray error:", e)

    def woke():
        print("WAKE detected")
        threading.Thread(target=handle_one_command, args=(hud,), daemon=True).start()

    listener = PorcupineListener(
        keyword="jarvis",
        on_wake=woke,
        sensitivity=WAKE_SENS
    )
    listener.start()

    print("Jarvis ready. Say 'Jarvis' to wake.")

    try:
        while True:
            time.sleep(0.2)
    except KeyboardInterrupt:
        listener.stop()
        hud.stop()
        sys.exit(0)


if __name__ == "__main__":
    run_loop()
