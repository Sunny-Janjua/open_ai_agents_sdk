"""Generate 100 agent template files grouped by category."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "agents_100"

CATEGORY_OVERVIEW = {
    "developer_agents": "Build and maintain software systems with strong engineering quality.",
    "learning_agents": "Help users learn faster with tutoring, quizzes, and study workflows.",
    "business_agents": "Support business operations like sales, support, and market analysis.",
    "social_media_agents": "Create and manage social media content and engagement.",
    "writing_agents": "Draft, edit, and improve written content across formats.",
    "productivity_agents": "Organize work, time, notes, and task execution.",
    "money_making_agents": "Assist with opportunity discovery, analysis, and revenue workflows.",
    "web_automation_agents": "Automate web tasks like scraping, form handling, and testing.",
    "advanced_ai_agents": "Use advanced planning, memory, and autonomous multi-step behavior.",
    "real_world_agents": "Domain-focused assistants for practical real-world jobs.",
}

AGENTS: dict[str, list[str]] = {
    "developer_agents": [
        "Code Generator Agent",
        "Bug Fixing Agent",
        "Code Reviewer Agent",
        "API Builder Agent",
        "SQL Query Generator Agent",
        "Documentation Writer Agent",
        "Test Case Generator Agent",
        "Refactoring Agent",
        "DevOps Deployment Agent",
        "Git Commit Message Writer Agent",
    ],
    "learning_agents": [
        "Personal Tutor Agent",
        "Quiz Generator Agent",
        "Flashcard Maker Agent",
        "Study Planner Agent",
        "Exam Preparation Agent",
        "Concept Explainer Agent",
        "Coding Teacher Agent",
        "Interview Preparation Agent",
        "MCQ Generator Agent",
        "Assignment Solver Agent",
    ],
    "business_agents": [
        "Customer Support Agent",
        "Sales Agent",
        "Lead Generation Agent",
        "Email Reply Agent",
        "Meeting Scheduler Agent",
        "CRM Update Agent",
        "Invoice Generator Agent",
        "Market Research Agent",
        "Competitor Analysis Agent",
        "Proposal Writer Agent",
    ],
    "social_media_agents": [
        "Instagram Post Creator Agent",
        "LinkedIn Content Creator Agent",
        "Twitter Post Writer Agent",
        "YouTube Script Writer Agent",
        "Caption Generator Agent",
        "Hashtag Generator Agent",
        "Comment Reply Agent",
        "Social Media Manager Agent",
        "Viral Content Finder Agent",
        "Trend Analyzer Agent",
    ],
    "writing_agents": [
        "Blog Writer Agent",
        "Story Writer Agent",
        "Book Writer Agent",
        "Poetry Writer Agent",
        "Resume Builder Agent",
        "Cover Letter Agent",
        "Email Writer Agent",
        "Copywriting Agent",
        "Proofreading Agent",
        "Grammar Corrector Agent",
    ],
    "productivity_agents": [
        "Personal Assistant Agent",
        "Reminder Agent",
        "Task Manager Agent",
        "Calendar Manager Agent",
        "Note Taking Agent",
        "File Organizer Agent",
        "Automation Agent",
        "Research Agent",
        "Decision Helper Agent",
        "Time Planner Agent",
    ],
    "money_making_agents": [
        "Freelance Finder Agent",
        "Fiverr Gig Agent",
        "Upwork Bidding Agent",
        "Product Research Agent",
        "Dropshipping Agent",
        "Affiliate Marketing Agent",
        "Crypto Trading Agent",
        "Stock Analysis Agent",
        "Price Comparison Agent",
        "Deal Finder Agent",
    ],
    "web_automation_agents": [
        "Web Scraping Agent",
        "Data Extraction Agent",
        "Form Filling Agent",
        "Website Testing Agent",
        "Browser Automation Agent",
        "Job Apply Agent",
        "News Collector Agent",
        "Email Automation Agent",
        "Login Automation Agent",
        "Screenshot Agent",
    ],
    "advanced_ai_agents": [
        "Multi-Agent System Agent",
        "Autonomous Agent",
        "Research Agent",
        "Planning Agent",
        "Decision Making Agent",
        "Memory Based Agent",
        "Tool Using Agent",
        "Self Improving Agent",
        "Workflow Automation Agent",
        "Personal AI Assistant Agent",
    ],
    "real_world_agents": [
        "Doctor Assistant Agent",
        "Lawyer Assistant Agent",
        "Teacher Assistant Agent",
        "Programmer Assistant Agent",
        "YouTube Automation Agent",
        "Ecommerce Assistant Agent",
        "HR Hiring Agent",
        "Startup Idea Generator Agent",
        "Life Coach Agent",
        "Full Personal Jarvis Agent",
    ],
}


def slugify(text: str) -> str:
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def render_agent_file(name: str, category: str, overview: str) -> str:
    return f'''"""Auto-generated template: {name}."""

from agents import Agent


def build_agent() -> Agent:
    return Agent(
        name="{name}",
        instructions=(
            "You are the {name}. "
            "Primary domain: {category}. "
            "Objective: {overview} "
            "Use this workflow: "
            "1) Understand user goal and constraints. "
            "2) Ask clarifying questions when requirements are missing. "
            "3) Produce a clear, actionable result. "
            "4) Highlight risks, assumptions, and next steps."
        ),
    )


agent = build_agent()


if __name__ == "__main__":
    print(f"{{agent.name}} ready")
'''


def main() -> None:
    OUT.mkdir(exist_ok=True)
    total = 0
    readme_lines = [
        "# 100 AI Agent Templates",
        "",
        "Generated from your 100 ideas list.",
        "",
        "## Structure",
        "",
    ]

    for category, names in AGENTS.items():
        category_dir = OUT / category
        category_dir.mkdir(parents=True, exist_ok=True)
        (category_dir / "__init__.py").write_text("", encoding="utf-8")
        overview = CATEGORY_OVERVIEW[category]
        readme_lines.append(f"- `{category}` ({len(names)} files)")

        for idx, name in enumerate(names, start=1):
            file_name = f"{idx:02d}_{slugify(name)}.py"
            path = category_dir / file_name
            path.write_text(
                render_agent_file(
                    name=name,
                    category=category.replace("_", " "),
                    overview=overview,
                ),
                encoding="utf-8",
            )
            total += 1

    (OUT / "__init__.py").write_text("", encoding="utf-8")
    readme_lines.extend(
        [
            "",
            f"Total agent files: **{total}**",
            "",
            "## Run Example",
            "",
            "```bash",
            "python agents_100/developer_agents/01_code_generator_agent.py",
            "```",
        ]
    )
    (OUT / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")
    print(f"Generated {total} agent files in {OUT}")


if __name__ == "__main__":
    main()

