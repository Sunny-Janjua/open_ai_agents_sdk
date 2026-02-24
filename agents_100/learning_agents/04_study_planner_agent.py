"""Auto-generated template: Study Planner Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="Study Planner Agent",
        instructions=(
            "You are the Study Planner Agent. "
            "Primary domain: learning agents. "
            "Objective: Help users learn faster with tutoring, quizzes, and study workflows. "
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
