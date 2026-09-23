from datetime import datetime
import os
import json

from groq import AsyncGroq

from intelligence.schema import Intent


INTENT_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {
            "type": "string"
        },
        "task": {
            "type": "string"
        },
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": ["string", "null"]
                },
                "time": {
                    "type": ["string", "null"]
                },
                "location": {
                    "type": ["string", "null"]
                },
                "title": {
                    "type": ["string", "null"]
                },
                "content": {
                    "type": ["string", "null"]
                }
            },
            "required": [
                "date",
                "time",
                "location",
                "title",
                "content"
            ],
            "additionalProperties": False
        },
        "missing_information": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "requires_confirmation": {
            "type": "boolean"
        }
    },
    "required": [
        "intent",
        "task",
        "parameters",
        "missing_information",
        "requires_confirmation"
    ],
    "additionalProperties": False
}


class LLM:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY", "").strip()

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set in the environment."
            )

        self.client = AsyncGroq(
            api_key=api_key
        )

        self.model = os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

    async def understand(self, user_input: str) -> Intent:

        current_dt = datetime.now().strftime("%Y-%m-%d %H:%M (%A)")

        system_prompt = f"""You are the reasoning and understanding layer of ARIA, an autonomous personal AI assistant.
Current Date & Time: {current_dt}

Convert the user's request into the provided structured schema.

Rules:
1. Identify the user's intended action (use standard action verbs like 'set_reminder', 'create_reminder').
2. Extract relevant parameters:
   - For dates: Convert relative terms ('today', 'tomorrow', 'next Monday', etc.) to 'YYYY-MM-DD' based on the Current Date & Time.
   - For times: Extract time in 'HH:MM' (or 12-hour AM/PM) format if provided, otherwise null.
   - For title/task: Extract a concise summary of what needs to be done.
3. Never invent completely unmentioned information, but always resolve relative temporal expressions using the Current Date & Time.
4. Put genuinely missing required information (e.g. if no date/time is specified and none can be inferred) into missing_information.
5. Do not execute the task.
6. Return only the requested structured object.
"""

        response = await self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],

            temperature=0,

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "aria_intent",
                    "schema": INTENT_SCHEMA
                }
            }
        )

        data = json.loads(
            response.choices[0].message.content
        )

        return Intent.model_validate(data)