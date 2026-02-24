"""Auto-generated template: Decision Helper Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Decision Helper Agent",
        instructions=(
            "You are the Decision Helper Agent. "
            "Primary domain: productivity agents. "
            "Objective: Organize work, time, notes, and task execution. "
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
