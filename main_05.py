"""Level 5: Sessions and memory with SQLiteSession."""

import asyncio

from agents import Agent, Runner, SQLiteSession


async def main() -> None:
    agent = Agent(
        name="MemoryAssistant",
        instructions="Use conversation context and answer briefly.",
    )
    session = SQLiteSession("demo_user_001")

    r1 = await Runner.run(agent, "I am planning a 5-day trip to Japan.", session=session)
    print("Turn 1:", r1.final_output)

    r2 = await Runner.run(agent, "What country did I mention?", session=session)
    print("Turn 2:", r2.final_output)


if __name__ == "__main__":
    asyncio.run(main())

