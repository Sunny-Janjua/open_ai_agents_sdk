"""Level 1: Your first agent."""

from agents import Agent, Runner


def main() -> None:
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Keep responses concise.",
    )
    result = Runner.run_sync(agent, "Give me one tip to learn Python faster.")
    print(result.final_output)


if __name__ == "__main__":
    main()

