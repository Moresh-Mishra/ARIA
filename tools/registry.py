from tools.reminder import create_reminder


TOOLS = {
    "create_reminder": create_reminder,
    "set_reminder": create_reminder,
    "reminder": create_reminder,
    "add_reminder": create_reminder,
    "schedule_reminder": create_reminder,
}


def get_tool(name: str):
    if not name:
        return None
    normalized = name.lower().strip().replace(" ", "_").replace("-", "_")
    return TOOLS.get(normalized)