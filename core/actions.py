import os
import webbrowser
import platform

def run_action_from_text(t):
    t = t.lower()

    if "chrome" in t or "browser" in t:
        if platform.system() == "Windows":
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        else:
            webbrowser.open("https://google.com")
        return "Opening browser."

    if "notepad" in t:
        if platform.system() == "Windows":
            os.startfile("notepad.exe")
        return "Opening notepad."

    if "youtube" in t:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

    return None
