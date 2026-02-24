"""Level 10: Model selection and run-level override."""

from agents import Agent, ModelSettings, RunConfig, Runner


def main() -> None:
    fast_agent = Agent(
        name="FastAgent",
        instructions="Answer in short bullet points.",
        model="gpt-4.1",
        model_settings=ModelSettings(temperature=0.2),
    )
    r1 = Runner.run_sync(fast_agent, "Give 3 quick API reliability tips.")
    print("Fast agent:\n", r1.final_output)

    default_agent = Agent(
        name="DefaultAgent",
        instructions="Answer clearly with concrete examples.",
    )
    r2 = Runner.run_sync(
        default_agent,
        "Explain exponential backoff with one simple example.",
        run_config=RunConfig(model="gpt-5.2"),
    )
    print("\nRun-level model override:\n", r2.final_output)


if __name__ == "__main__":
    main()

