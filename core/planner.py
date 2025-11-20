# core/planner.py
#
# Converts intent → plan_steps (actions + params)
# Used by brain.py for executing tools in correct order.

from core.utils import extract_number_from, parse_mouse_movement

def plan_for(intent: str, text: str):
    """
    Returns:
    {
        "plan_steps": [ { action:"...", params:{...} } ],
        "requires_confirmation": True/False
    }
    """

    # -------------------------------
    # CHANGE VOLUME
    # -------------------------------
    if intent == "change_volume":
        return {
            "plan_steps": [
                {
                    "action": "set_volume",
                    "params": {"percent": extract_number_from(text, default=50)}
                }
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # CHANGE BRIGHTNESS
    # -------------------------------
    if intent == "change_brightness":
        return {
            "plan_steps": [
                {
                    "action": "set_brightness",
                    "params": {"percent": extract_number_from(text, default=50)}
                }
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # MOUSE CONTROL
    # -------------------------------
    if intent == "mouse_control":
        return {
            "plan_steps": [
                {
                    "action": "mouse_move",
                    "params": parse_mouse_movement(text)
                }
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # TAKE SCREENSHOT
    # -------------------------------
    if intent == "take_screenshot":
        return {
            "plan_steps": [
                {
                    "action": "screenshot",
                    "params": {"path": "screenshot.png"}
                }
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # SYSTEM SHUTDOWN
    # -------------------------------
    if intent == "system_shutdown":
        return {
            "plan_steps": [
                {
                    "action": "shutdown",
                    "params": {"confirm": True}
                }
            ],
            "requires_confirmation": True
        }

    # -------------------------------
    # SYSTEM RESTART
    # -------------------------------
    if intent == "system_restart":
        return {
            "plan_steps": [
                {
                    "action": "restart",
                    "params": {"confirm": True}
                }
            ],
            "requires_confirmation": True
        }

    # -------------------------------
    # RAG SEARCH
    # -------------------------------
    if intent == "rag_search":
        return {
            "plan_steps": [
                {"action": "rag_search", "params": {"query": text}}
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # RAG INGEST
    # -------------------------------
    if intent == "rag_ingest":
        return {
            "plan_steps": [
                {"action": "rag_ingest", "params": {"file": text}}
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # MEMORY ADD
    # -------------------------------
    if intent == "memory_add":
        return {
            "plan_steps": [
                {"action": "memory_add", "params": {"text": text}}
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # MEMORY FORGET
    # -------------------------------
    if intent == "memory_forget":
        return {
            "plan_steps": [
                {"action": "memory_forget", "params": {"text": text}}
            ],
            "requires_confirmation": False
        }

    # -------------------------------
    # GENERAL CHAT (Default)
    # -------------------------------
    return {
        "plan_steps": [
            {"action": "chat", "params": {"query": text}}
        ],
        "requires_confirmation": False
    }
