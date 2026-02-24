"""Auto-generated template: News Collector Agent."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="News Collector Agent",
        instructions=(
            "You are the News Collector Agent. "
            "Primary domain: web automation agents. "
            "Objective: Automate web tasks like scraping, form handling, and testing. "
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
