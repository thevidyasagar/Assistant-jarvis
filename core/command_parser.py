# core/command_parser.py
#
# Simple rule-based command parser for Jarvis
# Detects apps, websites, system commands, music, etc.

import webbrowser
import os

def open_app(name):
    name = name.lower()

    # Windows apps
    if name in ["notepad", "editor"]:
        os.system("start notepad")
        return "Opening Notepad."

    if name in ["calculator", "calc"]:
        os.system("start calc")
        return "Opening Calculator."

    if name in ["paint", "mspaint"]:
        os.system("start mspaint")
        return "Opening Paint."

    # Browsers
    if name in ["chrome", "google chrome"]:
        os.system("start chrome")
        return "Opening Chrome."

    if name in ["edge", "microsoft edge"]:
        os.system("start msedge")
        return "Opening Edge."

    return None


def open_website(text):
    text = text.lower()

    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "whatsapp": "https://web.whatsapp.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "gmail": "https://mail.google.com",
    }

    for key, url in sites.items():
        if key in text:
            webbrowser.open(url)
            return f"Opening {key}."

    return None


def run_action_from_text(text):
    text = text.lower()

    # 1. OPEN WEBSITE
    if "open" in text or "khol" in text or "chod" in text or "chalao" in text:
        site = open_website(text)
        if site:
            return site

    # 2. OPEN APP
        words = ["chrome", "notepad", "calculator", "paint", "editor", "calc", "mspaint"]
        for w in words:
            if w in text:
                return open_app(w)

    # 3. System actions
    if "shutdown" in text or "band karo" in text:
        os.system("shutdown /s /t 3")
        return "Shutting down your PC."

    if "restart" in text or "reboot" in text:
        os.system("shutdown /r /t 3")
        return "Restarting your PC."

    # 4. Volume control
    if "volume" in text:
        if "up" in text or "increase" in text or "zyada" in text:
            os.system("nircmd.exe changesysvolume 5000")
            return "Increasing volume."
        if "down" in text or "decrease" in text or "kam" in text:
            os.system("nircmd.exe changesysvolume -5000")
            return "Decreasing volume."

    return None
