"""
memory_engine.py — Personalized Memory System for Jarvis
Stores: preferences, habits, notes, reminders, context
"""

import json
import os
from datetime import datetime

MEM_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent", "personal_memory.json")


# ----------------------------------
# Load / Save Memory
# ----------------------------------

def load_memory():
    try:
        with open(MEM_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "preferences": {},
            "habits": {},
            "notes": [],
            "reminders": [],
            "history": []
        }


def save_memory(data):
    with open(MEM_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ----------------------------------
# Add items
# ----------------------------------

def remember_preference(key, value):
    mem = load_memory()
    mem["preferences"][key] = value
    save_memory(mem)
    return True


def remember_habit(habit_name, data):
    mem = load_memory()
    mem["habits"][habit_name] = data
    save_memory(mem)
    return True


def add_note(note_text):
    mem = load_memory()
    mem["notes"].append({
        "text": note_text,
        "time": datetime.now().isoformat()
    })
    save_memory(mem)
    return True


def add_history(entry_text):
    mem = load_memory()
    mem["history"].append({
        "entry": entry_text,
        "time": datetime.now().isoformat()
    })
    save_memory(mem)
    return True


# ----------------------------------
# Querying memory
# ----------------------------------

def get_preference(key):
    return load_memory().get("preferences", {}).get(key)


def get_habit(habit_name):
    return load_memory().get("habits", {}).get(habit_name)


def search_notes(keyword):
    mem = load_memory()
    keyword = keyword.lower()
    return [n for n in mem["notes"] if keyword in n["text"].lower()]


def get_history(limit=5):
    mem = load_memory()
    return mem["history"][-limit:]
