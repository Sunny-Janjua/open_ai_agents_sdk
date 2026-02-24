"""Auto-generated template: Dropshipping Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Dropshipping Agent",
        instructions=(
            "You are the Dropshipping Agent. "
            "Primary domain: money making agents. "
            "Objective: Assist with opportunity discovery, analysis, and revenue workflows. "
            "Use this workflow: "
            "1) Understand user goal and constraints. "
            "2) Ask clarifying questions when requirements are missing. "
            "3) Produce a clear, actionable result. "
            "4) Highlight risks, assumptions, and next steps."
        ),
    )


agent = build_agent()


if __name__ == "__main__":
    print(f"{agent.name} ready")
