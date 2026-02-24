"""Level 7: Guardrails (input guardrail example)."""

import asyncio

from pydantic import BaseModel

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)


class HomeworkCheck(BaseModel):
    is_homework: bool
    reasoning: str


guardrail_checker = Agent(
    name="HomeworkGuardrail",
    instructions="Detect if the user is asking for direct homework answers.",
    output_type=HomeworkCheck,
)


@input_guardrail
async def homework_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    user_input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
    check = await Runner.run(guardrail_checker, user_input, context=ctx.context)
    output = check.final_output
    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=output.is_homework,
    )


async def main() -> None:
    tutor = Agent(
        name="Tutor",
        instructions="Help users learn but do not solve disallowed requests.",
        input_guardrails=[homework_input_guardrail],
    )

    allowed = await Runner.run(tutor, "Explain what recursion is with a simple analogy.")
    print("Allowed:", allowed.final_output)

    try:
        await Runner.run(tutor, "Solve my graded math homework problem 2 exactly.")
    except InputGuardrailTripwireTriggered as exc:
        print("Blocked by guardrail:", exc)


if __name__ == "__main__":
    asyncio.run(main())

