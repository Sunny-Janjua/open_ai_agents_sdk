"""18 Advanced: MCP prompts example."""

from _compat import MCPServer

mcp = MCPServer("server-18-prompts")


@mcp.prompt()
def summarize_prompt(topic: str) -> str:
    return (
        "You are an expert educator.\n"
        f"Summarize '{topic}' for a beginner in 5 bullet points.\n"
        "Include one real-world example."
    )


@mcp.prompt()
def code_review_prompt(language: str, code: str) -> str:
    return (
        f"Review this {language} code for correctness, readability, and security.\n"
        "Return findings sorted by severity.\n\n"
        f"{code}"
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

