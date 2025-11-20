"""
tools.py — Tool Execution Layer for Jarvis
Each tool = a function that performs a real action.
Planner uses these tool names in plan_steps.
"""

from core.actions import run_action_from_text
from core.memory import add_memory
from rag.rag_engine import ingest_file, search as rag_search


# -------------------------------
# BASIC TOOLS
# -------------------------------
def tool_rag_search(params):
    q = params.get("query")
    results = rag_search(q)
    return {"ok": True, "result": "\n\n---\n".join(results)}


def tool_run_action(params):
    text = params.get("text", "")
    result = run_action_from_text(text)
    if result:
        return {"ok": True, "result": result}
    return {"ok": False, "error": "Unknown action"}

def tool_search(params):
    query = params.get("query") or params.get("text")
    if not query:
        return {"ok": False, "error": "No query provided"}

    import webbrowser
    webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))

    return {"ok": True, "result": f"Searching Google for: {query}"}

def tool_create_note(params):
    text = params.get("text") or "(empty note)"
    note = add_memory("notes", text)
    return {"ok": True, "result": f"Note saved: {text}", "id": note["id"]}

def tool_create_reminder(params):
    title = params.get("title") or params.get("text")
    time_value = params.get("datetime")
    
    reminder = add_memory("reminders", {
        "title": title,
        "time": time_value
    })

    return {
        "ok": True,
        "result": f"Reminder set: {title}",
        "id": reminder["id"]
    }

# Future expansion
def tool_send_message(params):
    text = params.get("text", "")
    # Real WhatsApp / SMS integration in Module-3
    fake_reply = f"Message prepared: {text}"
    return {"ok": True, "result": fake_reply}

def tool_summarize(params):
    from core.llm import ask_chat
    data = params.get("text")
    res = ask_chat("Summarize this:\n" + data)
    return {"ok": True, "result": res}

# -------------------------------
# TOOL REGISTRY
# -------------------------------

TOOL_REGISTRY = {
    "run_action": tool_run_action,
    "search": tool_search,
    "create_note": tool_create_note,
    "create_reminder": tool_create_reminder,
    "send_message": tool_send_message,
    "summarize": tool_summarize,
    "rag_search": tool_rag_search,

}

def run_tool(action, params):
    func = TOOL_REGISTRY.get(action)
    if not func:
        return {"ok": False, "error": f"Unknown tool: {action}"}

    try:
        return func(params)
    except Exception as e:
        return {"ok": False, "error": str(e)}
