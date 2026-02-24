"""Auto-generated template: Life Coach Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Life Coach Agent",
        instructions=(
            "You are the Life Coach Agent. "
            "Primary domain: real world agents. "
            "Objective: Domain-focused assistants for practical real-world jobs. "
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
