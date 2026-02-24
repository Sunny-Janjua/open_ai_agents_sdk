"""Level 2: Async run and manual multi-turn state."""

import asyncio

from agents import Agent, Runner


async def main() -> None:
    agent = Agent(
        name="Assistant",
        instructions="Answer clearly in 1-2 sentences.",
    )

    first = await Runner.run(agent, "Golden Gate Bridge is in which city?")
    print("First:", first.final_output)

    follow_up_input = first.to_input_list() + [
        {"role": "user", "content": "What state is that city in?"}
    ]
    second = await Runner.run(agent, follow_up_input)
    print("Second:", second.final_output)


if __name__ == "__main__":
    asyncio.run(main())

