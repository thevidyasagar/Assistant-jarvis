# core/stt.py — GPU accelerated whisper using faster-whisper

from faster_whisper import WhisperModel

# Load model one time (use "small" or "base" for best real-time speed)
model = WhisperModel(
    "small",
    device="cuda",
    compute_type="float16"   # use GPU FP16 compute
)

def transcribe_file(path):
    segments, info = model.transcribe(path, beam_size=5)
    text = " ".join(seg.text for seg in segments)
    return text
