"""Level 3: Structured output with Pydantic."""

from pydantic import BaseModel

from agents import Agent, Runner


class TicketSummary(BaseModel):
    priority: str
    summary: str
    needs_human: bool


def main() -> None:
    agent = Agent(
        name="SupportSummarizer",
        instructions="Summarize support text into structured triage fields.",
        output_type=TicketSummary,
    )
    result = Runner.run_sync(
        agent,
        "Customer says payment failed twice and account access is blocked.",
    )
    print(result.final_output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

