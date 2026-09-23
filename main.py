import asyncio
from dotenv import load_dotenv

from core.runtime import SakhaRuntime


async def main():

    load_dotenv()

    sakha = SakhaRuntime()

    print("ARIA online.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in {
            "exit",
            "quit"
        }:
            break

        if not user_input.strip():
            continue

        intent, decision, execution = await sakha.process(
            user_input
        )

        print("\n--- GEMINI / LLM ---")
        print(intent.model_dump_json(indent=2))

        print("\n--- LAYA ---")
        print(decision)

        print("\n--- EXECUTION ---")
        print(execution)

        if execution.get("success"):
            res = execution.get("result", {})
            print(f"\nARIA: Reminder set for '{res.get('title')}' on {res.get('date')} (time: {res.get('time') or 'not specified'}).")
        elif execution.get("requires_confirmation"):
            print("\nARIA: Action requires explicit confirmation before execution.")
        else:
            print(f"\nARIA: Could not complete task. Error: {execution.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())