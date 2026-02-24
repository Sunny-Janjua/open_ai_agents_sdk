"""Auto-generated template: Resume Builder Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Resume Builder Agent",
        instructions=(
            "You are the Resume Builder Agent. "
            "Primary domain: writing agents. "
            "Objective: Draft, edit, and improve written content across formats. "
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
