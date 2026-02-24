"""Level 9: Streaming and usage metrics."""

import asyncio

from openai.types.responses import ResponseTextDeltaEvent

from agents import Agent, Runner


async def main() -> None:
    agent = Agent(
        name="Streamer",
        instructions="Give practical software engineering advice.",
    )

    streamed = Runner.run_streamed(
        agent,
        input="Share 5 concise tips to write maintainable Python code.",
    )

    print("Streaming output:")
    async for event in streamed.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print("\n")
    print("Final output:")
    print(streamed.final_output)

    usage = streamed.context_wrapper.usage
    print("\nUsage:")
    print("requests:", getattr(usage, "requests", None))
    print("input_tokens:", getattr(usage, "input_tokens", None))
    print("output_tokens:", getattr(usage, "output_tokens", None))
    print("total_tokens:", getattr(usage, "total_tokens", None))


if __name__ == "__main__":
    asyncio.run(main())

