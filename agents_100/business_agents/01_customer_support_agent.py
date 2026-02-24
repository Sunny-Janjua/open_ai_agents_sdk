"""Auto-generated template: Customer Support Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Customer Support Agent",
        instructions=(
            "You are the Customer Support Agent. "
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
