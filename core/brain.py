# core/brain.py
# High-level reasoning core (Intent → Plan → Tools → Response)

from core.intent import detect_intent
from core.planner import plan_for
from core.tools import run_tool
from core.llm import ask_chat


def handle_user_text(text: str, ask_confirm_fn=None):
    """
    Main brain pipeline:
    1. Detect intent
    2. Generate plan
    3. Auto language detection (Hindi / English)
    4. Execute tools or fallback chat
    """

    # -----------------------------------------
    # LANGUAGE DETECTION
    # -----------------------------------------
    lower = text.lower()

    hindi_keywords = [
        "kya", "hai", "kaise", "kar", "mera", "tum",
        "bata", "kholo", "chalu", "band", "dikhao",
        "hindi", "jarvis", "open karo"
    ]

    use_hindi = any(w in lower for w in hindi_keywords)

    # ----------------------------------------------------------------
    # Step 1 — detect intent
    # ----------------------------------------------------------------
    intent_data = detect_intent(text)
    intent = intent_data.get("intent", "general_chat")

    # ----------------------------------------------------------------
    # Step 2 — build plan
    # ----------------------------------------------------------------
    plan = plan_for(intent, text)

    # ----------------------------------------------------------------
    # Step 3 — No-plan → fallback chat (Hindi or English)
    # ----------------------------------------------------------------
    if not plan:

        system = (
            "Tum Jarvis ho. Hammesha simple aur smooth Hindi me baat karo."
            if use_hindi else
            "You are Jarvis. Always reply in clean and conversational English."
        )

        reply = ask_chat(text, system_prompt=system)

        return {
            "status": "ok",
            "results": [
                {"type": "chat", "reply": reply}
            ]
        }

    # ----------------------------------------------------------------
    # Step 4 — Confirmation if needed
    # ----------------------------------------------------------------
    if plan.get("requires_confirmation") and ask_confirm_fn:
        question = plan.get("confirmation_prompt", "Should I continue?")
        ok = ask_confirm_fn(question)
        if not ok:
            return {"status": "cancelled"}

    # ----------------------------------------------------------------
    # Step 5 — Execute plan steps
    # ----------------------------------------------------------------
    results = []

    for step in plan.get("plan_steps", []):
        action = step.get("action")
        params = step.get("params", {})

        if not action:
            continue

        # Chat-style step
        if action == "chat":
            msg = params.get("text", "")

            system = (
                "Tum Jarvis ho. Hammesha simple aur smooth Hindi me baat karo."
                if use_hindi else
                "You are Jarvis. Always reply in clean conversational English."
            )

            reply = ask_chat(msg, system_prompt=system)
            results.append({"type": "chat", "reply": reply})

        # Tool execution
        else:
            tool_result = run_tool(action, params)
            results.append({"type": "tool", "result": tool_result})

    return {
        "status": "ok",
        "intent": intent,
        "results": results
    }
