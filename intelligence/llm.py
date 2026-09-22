import os

from google import genai

from intelligence.schema import Intent

class LLM:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the environment."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.6-flash"
        )

    async def understand(self, user_input: str) -> Intent:

        prompt = f"""
You are the reasoning and understanding layer of SAKHA,
an autonomous personal AI assistant.

Your job is to understand the user's request and convert it
into a structured task.

Rules:

1. Identify what the user wants to accomplish.
2. Extract relevant parameters.
3. If information is missing, put it in missing_information.
4. Do not invent missing information.
5. Do not execute the task.
6. Do not provide explanations or conversational responses.
7. Return only the structured response matching the schema.

User:
{user_input}
"""

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Intent,
            },
        )

        return Intent.model_validate_json(response.text)