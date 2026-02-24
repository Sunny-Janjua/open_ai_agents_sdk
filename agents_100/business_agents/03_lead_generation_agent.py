"""Auto-generated template: Lead Generation Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Lead Generation Agent",
        instructions=(
            "You are the Lead Generation Agent. "
            "Primary domain: business agents. "
            "Objective: Support business operations like sales, support, and market analysis. "
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
