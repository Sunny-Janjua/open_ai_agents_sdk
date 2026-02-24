"""Auto-generated template: Comment Reply Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Comment Reply Agent",
        instructions=(
            "You are the Comment Reply Agent. "
            "Primary domain: social media agents. "
            "Objective: Create and manage social media content and engagement. "
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
