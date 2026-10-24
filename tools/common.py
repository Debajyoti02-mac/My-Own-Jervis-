def is_yes(answer) -> bool:
    return str(answer).strip().lower().strip(".!?, ") in ("yes", "y", "confirm", "send", "ok", "okay")