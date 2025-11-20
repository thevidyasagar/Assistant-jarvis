# test_wake.py
from core.wake_porcupine import PorcupineListener
def on_w():
    print("WAKE DETECTED")
lst = PorcupineListener(keyword="jarvis", on_wake=on_w, sensitivity=0.9)
lst.start()
try:
    while True:
        pass
except KeyboardInterrupt:
    lst.stop()
