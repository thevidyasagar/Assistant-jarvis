"""
intent.py – Advanced Hinglish Intent Detection
Rule-based + LLM fallback
"""

from core.llm import ask_chat

# --------------------------------------------
# INTENT KEYWORD DICTIONARY (Hinglish + English)
# --------------------------------------------
INTENT_KEYWORDS = {
    "open_app": [
        "open", "start", "launch", "khol", "kholo", "chalana", "chalao", "run"
    ],
    "search_web": [
        "search", "find", "dhundo", "kya hai", "browse", "google karo", "search karo"
    ],
    "play_music": [
        "music", "song", "gaana", "play music", "music chalao", "gaana bajao"
    ],
    "create_note": [
        "note", "write down", "likh lo", "note kar", "note banao"
    ],
    "set_reminder": [
        "remind", "yaad", "reminder", "yaad dilao", "reminder lagao"
    ],
    "send_message": [
        "send", "message", "text", "sms", "bhejo", "whatsapp"
    ],
    "get_summary": [
        "summary", "summarize", "short version", "mukhtasar", "saar"
    ],
    "change_volume": [
        "volume", "sound", "awaz", "aavaj", "loud", "slow", "%", "percent",
        "thoda", "kam", "badha", "increase", "decrease", "voice"
    ],
    "change_brightness": [
        "brightness", "roshni", "light", "screen light", "dim", "bright",
        "full", "half", "kam", "badha", "zyada"
    ],
    "mouse_control": [
        "mouse", "cursor", "move", "drag", "right side", "left side", "upar",
        "neeche", "shift", "cursor ko"
    ],
    "take_screenshot": [
        "screenshot", "screen shot", "capture screen", "photo lo"
    ],
    "system_shutdown": [
        "shutdown", "band karo", "power off"
    ],
    "system_restart": [
        "restart", "reboot", "dobara chalu karo"
    ],
    "rag_ingest": [
        "ingest", "load file", "yaad rakho", "store file", "add document", "add pdf"
    ],
    "rag_search": [
        "document search", "rag search", "search document"
    ],
    "memory_add": [
        "remember this", "yaad rakho"
    ],
    "memory_forget": [
        "forget this", "bhool jao"
    ],
    "general_chat": []
}


# --------------------------------------------
# RULE-BASED INTENT MATCHING
# --------------------------------------------
def rule_based_intent(text: str):
    t = text.lower()
    scores = {}

    for intent, words in INTENT_KEYWORDS.items():
        score = 0
        for w in words:
            if w in t:
                score += 1
        scores[intent] = score

    # Pick best match
    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    # Confidence scale
    confidence = min(0.9, 0.2 + best_score * 0.25)

    return {
        "intent": best_intent,
        "confidence": confidence,
        "scores": scores
    }


# --------------------------------------------
# LLM FALLBACK INTENT
# --------------------------------------------
def llm_fallback_intent(text: str):
    system_prompt = (
        "You are an intent classifier. "
        "Classify the user query into exactly one intent: "
        "open_app, search_web, play_music, create_note, set_reminder, "
        "send_message, get_summary, general_chat.\n"
        "Respond ONLY in JSON like: {\"intent\":\"...\", \"confidence\":0.xx}"
    )

    raw = ask_chat(text, system_prompt=system_prompt)
    import json

    try:
        return json.loads(raw)
    except:
        return {"intent": "general_chat", "confidence": 0.4}


# --------------------------------------------
# FINAL INTENT DETECTOR
# --------------------------------------------
def detect_intent(text: str):
    rule = rule_based_intent(text)

    # If rule confidence is weak → fallback to LLM
    if rule["confidence"] < 0.3:
        return llm_fallback_intent(text)

    return rule
