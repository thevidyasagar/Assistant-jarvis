"""
wake_porcupine.py
Porcupine-based wake-word listener with safe fallback.
"""

import threading
import time
import sys

class PorcupineListener:
    def __init__(self, keyword="jarvis", on_wake=None, sensitivity=0.5, frame_length=None):
        """
        keyword: built-in keyword name (e.g. "jarvis", "hey google")
        on_wake: callback function when wake word is detected
        sensitivity: 0.0–1.0
        """
        self.keyword = keyword
        self.on_wake = on_wake
        self.sensitivity = float(sensitivity)
        self._thread = None
        self._stop_event = threading.Event()
        self._running = False
        self._cooldown = 1.0  # avoid repeat triggers

    def start(self):
        if self._running:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._running = True

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        self._running = False

    def _run(self):
        try:
            import pvporcupine
            import pyaudio
        except Exception as e:
            print("Porcupine not available; keyboard fallback. Error:", e)
            self._keyboard_fallback()
            return

        porcupine = None
        pa = None
        stream = None

        try:
            # ⭐⭐⭐ ADD YOUR ACCESS KEY HERE ⭐⭐⭐
            ACCESS_KEY = "o6hhDjAUlcU5Hg76xEQfqG1CgBhbmkv22C6N6ihk5/dCkFS59NuN2g=="

            porcupine = pvporcupine.create(
                access_key=ACCESS_KEY,
                keywords=[self.keyword],
                sensitivities=[self.sensitivity]
            )

            pa = pyaudio.PyAudio()
            stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

            print(f"Porcupine listening for keyword '{self.keyword}' (sensitivity={self.sensitivity})")

            last_trigger = 0.0

            while not self._stop_event.is_set():
                try:
                    pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                except Exception:
                    time.sleep(0.01)
                    continue

                pcm16 = memoryview(pcm).cast('h')
                idx = porcupine.process(pcm16)

                if idx >= 0:
                    now = time.time()
                    if now - last_trigger < self._cooldown:
                        continue
                    last_trigger = now

                    try:
                        if callable(self.on_wake):
                            self.on_wake()
                    except Exception as cb_e:
                        print("Wake callback error:", cb_e)

        except Exception as e:
            print("Porcupine failed; fallback to keyboard. Error:", e)
            self._keyboard_fallback()

        finally:
            try:
                if stream:
                    stream.stop_stream()
                    stream.close()
                if pa:
                    pa.terminate()
                if porcupine:
                    porcupine.delete()
            except Exception:
                pass

    def _keyboard_fallback(self):
        print("Keyboard fallback: Press Enter to wake Jarvis (Ctrl+C to exit).")
        try:
            while not self._stop_event.is_set():
                try:
                    input()
                except EOFError:
                    time.sleep(0.2)
                    continue
                if callable(self.on_wake):
                    self.on_wake()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
