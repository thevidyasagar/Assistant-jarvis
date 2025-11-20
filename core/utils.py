# core/utils.py
#
# Utility functions for planner, parsing numbers, mouse commands etc.

import re

# -----------------------------------------------------------
# EXTRACT NUMBER FROM TEXT
# Example: "volume 40 percent" → 40
# -----------------------------------------------------------
def extract_number_from(text: str, default=50):
    nums = re.findall(r"\d+", text)
    if not nums:
        return default
    try:
        val = int(nums[0])
        return max(0, min(100, val))
    except:
        return default


# -----------------------------------------------------------
# PARSE MOUSE MOVEMENT
# "move mouse left 200" → {"dx": -200, "dy": 0}
# "cursor ko neeche 100 le jao" → {"dx": 0, "dy": +100}
# -----------------------------------------------------------
def parse_mouse_movement(text: str):
    t = text.lower()

    # default
    dx = 0
    dy = 0

    # distance value
    nums = re.findall(r"\d+", t)
    amount = int(nums[0]) if nums else 50

    # LEFT
    if "left" in t or "daaye" in t or "left side" in t:
        dx = -amount

    # RIGHT
    if "right" in t or "dahine" in t or "right side" in t:
        dx = +amount

    # UP
    if "upar" in t or "up" in t:
        dy = -amount

    # DOWN
    if "neeche" in t or "down" in t:
        dy = +amount

    return {"dx": dx, "dy": dy}
