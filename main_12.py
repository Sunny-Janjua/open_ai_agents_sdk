"""Level 12: Realtime and Voice templates."""

import argparse
import asyncio

from agents import Agent


async def run_realtime_demo() -> None:
    try:
        from agents.realtime import RealtimeAgent, RealtimeRunner
    except Exception as exc:
        print("Realtime demo unavailable:", exc)
        print("Install/upgrade openai-agents and check realtime docs.")
        return

    agent = RealtimeAgent(
        name="RealtimeAssistant",
        instructions="Respond briefly and clearly.",
    )
    runner = RealtimeRunner(starting_agent=agent)

    try:
        session = await runner.run()
    except Exception as exc:
        print("Could not start realtime session:", exc)
        return

    print("Realtime session started. Listening for events (up to 10 events).")
    try:
        async with session:
            if hasattr(session, "send_message"):
                await session.send_message("Give one short tip for debugging Python.")
            count = 0
            async for event in session:
                event_type = getattr(event, "type", type(event).__name__)
                print("event:", event_type)
                delta = getattr(event, "delta", None)
                if delta:
                    print(delta, end="", flush=True)
                count += 1
                if count >= 10:
                    break
    except Exception as exc:
        print("\nRealtime event loop ended with:", exc)


async def run_voice_demo() -> None:
    try:
        import numpy as np
        from agents.voice import AudioInput, SingleAgentVoiceWorkflow, VoicePipeline
    except Exception as exc:
        print("Voice demo unavailable:", exc)
        print('Install optional deps, for example: pip install "openai-agents[voice]"')
        return

    agent = Agent(
        name="VoiceAssistant",
        instructions="Respond with practical, concise advice.",
    )
    workflow = SingleAgentVoiceWorkflow(agent)
    pipeline = VoicePipeline(workflow=workflow)

    # 2 seconds of silence at 24kHz (int16), used as a template input.
    buffer = np.zeros(2 * 24_000, dtype=np.int16)
    audio_input = AudioInput(buffer=buffer)

    try:
        result = await pipeline.run(audio_input)
        print("Voice run started. Streaming events:")
        async for event in result.stream():
            print("event:", getattr(event, "type", type(event).__name__))
    except Exception as exc:
        print("Voice pipeline could not run:", exc)


async def main(mode: str) -> None:
    if mode == "realtime":
        await run_realtime_demo()
    else:
        await run_voice_demo()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["realtime", "voice"], default="realtime")
    args = parser.parse_args()
    asyncio.run(main(args.mode))

