"""Level 8: Human in the loop (tool approval)."""

import asyncio

from agents import Agent, Runner, function_tool


@function_tool(needs_approval=True)
async def cancel_order(order_id: int) -> str:
    return f"Order {order_id} has been cancelled."


async def main() -> None:
    agent = Agent(
        name="SupportAgent",
        instructions="Use tools to handle support actions.",
        tools=[cancel_order],
    )

    result = await Runner.run(agent, "Cancel my order 1234.")

    while result.interruptions:
        state = result.to_state()
        for interruption in result.interruptions:
            print("Approval required:", interruption)
            # Replace with user-driven UI approval/rejection in real apps.
            state.approve(interruption)
        result = await Runner.run(agent, state)

    print("Final:", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())

