"""Level 4: Function tools."""

from agents import Agent, Runner, function_tool


@function_tool
def get_weather(city: str) -> str:
    return f"{city}: 25C, clear skies."


def main() -> None:
    agent = Agent(
        name="WeatherAssistant",
        instructions="Use tools when needed and keep answers brief.",
        tools=[get_weather],
    )
    result = Runner.run_sync(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    main()

