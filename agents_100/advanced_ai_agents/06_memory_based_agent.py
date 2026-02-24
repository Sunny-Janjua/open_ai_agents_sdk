"""Auto-generated template: Memory Based Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Memory Based Agent",
        instructions=(
            "You are the Memory Based Agent. "
            "Primary domain: advanced ai agents. "
            "Objective: Use advanced planning, memory, and autonomous multi-step behavior. "
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
