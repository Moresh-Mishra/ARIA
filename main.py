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

        response = await sakha.process(
            user_input
        )

        print("\nARIA:", response)
        print(response["intent"].model_dump_json(indent=2))

        print("\nLAYA DECISION:")
        print(response["decision"])


if __name__ == "__main__":
    asyncio.run(main())