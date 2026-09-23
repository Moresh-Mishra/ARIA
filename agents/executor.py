from tools.registry import get_tool


class AgentExecutor:

    async def execute(self, intent):

        tool = get_tool(intent.intent)

        if tool is None and intent.task:
            tool = get_tool(intent.task)

        if tool is None:
            return {
                "success": False,
                "error": f"No tool found for '{intent.intent}' (task: '{intent.task}')"
            }

        parameters = intent.parameters

        norm_intent = (intent.intent or "").lower().strip().replace(" ", "_").replace("-", "_")
        norm_task = (intent.task or "").lower().strip().replace(" ", "_").replace("-", "_")
        reminder_intents = {"set_reminder", "create_reminder", "reminder", "add_reminder", "schedule_reminder"}

        if norm_intent in reminder_intents or norm_task in reminder_intents:

            if not parameters.date:
                return {
                    "success": False,
                    "error": "Reminder date is missing."
                }

            result = tool(
                title=parameters.title or intent.task or "Reminder",
                date=parameters.date,
                time=parameters.time
            )

            return {
                "success": True,
                "result": result
            }

        return {
            "success": False,
            "error": f"Parameters not implemented for '{intent.intent}'."
        }