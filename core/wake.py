import sys

def wait_for_wake():
    """
    Wake-word detector.
    Falls back to Enter key if Porcupine is missing.
    """
    try:
        from pvporcupine import create as pv_create
        import pyaudio

        porcupine = pv_create(keywords=['jarvis'])
        pa = pyaudio.PyAudio()
        stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'Jarvis'...")

        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = memoryview(pcm).cast('h')
            result = porcupine.process(pcm)

            if result >= 0:
                print("Wake-word detected!")
                stream.stop_stream()
                stream.close()
                porcupine.delete()
                pa.terminate()
                return

    except Exception:
        print("Wake-word engine not found. Press Enter to wake.")
        input("Press Enter...")
