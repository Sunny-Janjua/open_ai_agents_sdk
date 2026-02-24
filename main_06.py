"""Level 6: Multi-agent orchestration (handoffs and agents-as-tools)."""

from agents import Agent, Runner


def handoff_demo() -> None:
    billing_agent = Agent(
        name="BillingAgent",
        instructions="Handle billing, invoices, charges, and refunds.",
    )
    tech_agent = Agent(
        name="TechAgent",
        instructions="Handle technical troubleshooting and product bugs.",
    )
    triage_agent = Agent(
        name="TriageAgent",
        instructions="Route users to the right specialist.",
        handoffs=[billing_agent, tech_agent],
    )
    result = Runner.run_sync(
        triage_agent,
        "I was charged twice for order A-123. Please help me get refunded.",
    )
    print("Handoff result:", result.final_output)
    print("Handled by:", result.last_agent.name)


def agent_as_tool_demo() -> None:
    flights_agent = Agent(
        name="FlightsAgent",
        instructions="You are a flights specialist.",
    )
    hotels_agent = Agent(
        name="HotelsAgent",
        instructions="You are a hotels specialist.",
    )
    orchestrator = Agent(
        name="TravelOrchestrator",
        instructions="Use tools to answer travel questions.",
        tools=[
            flights_agent.as_tool(
                tool_name="ask_flights",
                tool_description="Ask flight specialist.",
            ),
            hotels_agent.as_tool(
                tool_name="ask_hotels",
                tool_description="Ask hotel specialist.",
            ),
        ],
    )
    result = Runner.run_sync(orchestrator, "I need cheap flights and a central hotel in Tokyo.")
    print("Orchestrator result:", result.final_output)


def main() -> None:
    handoff_demo()
    print("-" * 40)
    agent_as_tool_demo()


if __name__ == "__main__":
    main()

