# core/memory.py
# Simple in-memory + disk persistence memory engine

import json
import os

MEM_FILE = "data/memory_store.json"


# Ensure memory file
def _ensure_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(MEM_FILE):
        with open(MEM_FILE, "w", encoding="utf-8") as f:
            json.dump({"memories": []}, f)


def add_memory(text: str):
    """Store a new memory string."""
    _ensure_file()

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"memories": []}

    data["memories"].append(text)

    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return {"ok": True, "result": f"Memory stored: {text}"}


def query_memory(query: str):
    """Search memories for text overlap / keyword match."""
    _ensure_file()

    try:
        with open(MEM_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        mems = data.get("memories", [])
    except:
        mems = []

    query_low = query.lower()
    matches = [m for m in mems if query_low in m.lower()]

    if not matches:
        return {"ok": True, "result": "No related memory found."}

    result = "\n".join(matches)
    return {"ok": True, "result": result}
