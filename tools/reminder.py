from datetime import datetime
from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REMINDER_FILE = PROJECT_ROOT / "data" / "reminders.json"


def create_reminder(
    title: str,
    date: str,
    time: str | None = None
):
    REMINDER_FILE.parent.mkdir(parents=True, exist_ok=True)

    reminders = []

    if REMINDER_FILE.exists():
        with open(REMINDER_FILE, "r", encoding="utf-8") as f:
            reminders = json.load(f)

    reminder = {
        "id": len(reminders) + 1,
        "title": title,
        "date": date,
        "time": time,
        "created_at": datetime.now().isoformat()
    }

    reminders.append(reminder)

    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)

    return reminder