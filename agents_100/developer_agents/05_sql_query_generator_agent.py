"""Auto-generated template: SQL Query Generator Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="SQL Query Generator Agent",
        instructions=(
            "You are the SQL Query Generator Agent. "
            "Primary domain: developer agents. "
            "Objective: Build and maintain software systems with strong engineering quality. "
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
