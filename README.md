# OpenAI Agents SDK (Python) - Complete Guide (Beginner to Advanced)

This guide is a practical, level-by-level path for learning and building with the OpenAI Agents SDK for Python.

It is based on the official docs: https://openai.github.io/openai-agents-python/

## Table of Contents

1. [What You Will Build](#what-you-will-build)
2. [Prerequisites](#prerequisites)
3. [Level 0 - Setup and First Run](#level-0---setup-and-first-run)
4. [Level 1 - Core Concepts](#level-1---core-concepts)
5. [Level 2 - Running Agents Correctly](#level-2---running-agents-correctly)
6. [Level 3 - Structured Outputs](#level-3---structured-outputs)
7. [Level 4 - Tools](#level-4---tools)
8. [Level 5 - Sessions and Memory](#level-5---sessions-and-memory)
9. [Level 6 - Multi-Agent Systems](#level-6---multi-agent-systems)
10. [Level 7 - Guardrails and Safety](#level-7---guardrails-and-safety)
11. [Level 8 - Human in the Loop (Approvals)](#level-8---human-in-the-loop-approvals)
12. [Level 9 - Streaming, Tracing, and Usage](#level-9---streaming-tracing-and-usage)
13. [Level 10 - Models and Performance Tuning](#level-10---models-and-performance-tuning)
14. [Level 11 - MCP Integration](#level-11---mcp-integration)
15. [Level 12 - Realtime and Voice Agents](#level-12---realtime-and-voice-agents)
16. [Production Checklist](#production-checklist)
17. [Copy-Paste Project Templates](#copy-paste-project-templates)
18. [2-Week Learning Plan](#2-week-learning-plan)
19. [Official References](#official-references)

## What You Will Build

By the end, you should be able to build:

- A single helpful assistant agent
- Multi-agent workflows with handoffs
- Tool-enabled agents (local + hosted tools)
- Safe systems with guardrails and approval gates
- Session-backed conversational apps
- Observable systems with streaming, tracing, and usage metrics
- Integrations with MCP servers
- Realtime/voice-capable agent apps

## Prerequisites

- Python 3.9+
- OpenAI API key
- Basic Python and async understanding

Install:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
pip install openai-agents
set OPENAI_API_KEY=sk-...
```

Optional extras:

```bash
pip install "openai-agents[litellm]"
pip install "openai-agents[voice]"
pip install "openai-agents[redis]"
```

## Level 0 - Setup and First Run

Goal: run your first agent end-to-end.

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant."
)

result = Runner.run_sync(agent, "Write one short tip to learn Python faster.")
print(result.final_output)
```

You learned:

- `Agent` defines behavior
- `Runner.run_sync` executes it
- `result.final_output` gives the final answer

## Level 1 - Core Concepts

Goal: understand the SDK mental model.

- `Agent`: instructions, model, tools, handoffs, guardrails
- `Runner`: execution engine
- `RunResult`: output + metadata + generated items
- Tools: actions agent can perform
- Handoffs: transfer work to another agent
- Sessions: persistent conversation history

## Level 2 - Running Agents Correctly

Goal: choose the right run mode.

- `Runner.run(...)`: async default for apps/services
- `Runner.run_sync(...)`: script-friendly
- `Runner.run_streamed(...)`: token/item streaming

Useful options:

- `max_turns`
- `run_config`
- `error_handlers`
- `hooks`

Manual multi-turn (without session):

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="Be concise.")
    result = await Runner.run(agent, "Golden Gate Bridge is in which city?")
    print(result.final_output)

    new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
    result = await Runner.run(agent, new_input)
    print(result.final_output)

asyncio.run(main())
```

## Level 3 - Structured Outputs

Goal: make agent responses reliable and machine-usable.

```python
from pydantic import BaseModel
from agents import Agent, Runner

class TicketSummary(BaseModel):
    priority: str
    summary: str
    needs_human: bool

agent = Agent(
    name="Support summarizer",
    instructions="Return structured triage fields.",
    output_type=TicketSummary
)

result = Runner.run_sync(agent, "Customer cannot access billing portal since yesterday.")
print(result.final_output)
```

Why this matters:

- Reduces parsing errors
- Enables deterministic routing in code
- Helps build robust pipelines

## Level 4 - Tools

Goal: let the agent perform real actions.

SDK tool categories:

- Hosted tools: `WebSearchTool`, `FileSearchTool`, `CodeInterpreterTool`, `HostedMCPTool`, `ImageGenerationTool`
- Local runtime tools: `ShellTool`, `ApplyPatchTool`, `ComputerTool`
- Function tools: `@function_tool`
- Agents as tools: `agent.as_tool(...)`

Basic function tool:

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"{city}: 25C, clear"

agent = Agent(
    name="Weather assistant",
    instructions="Use tools when useful.",
    tools=[get_weather]
)

result = Runner.run_sync(agent, "What is the weather in Tokyo?")
print(result.final_output)
```

## Level 5 - Sessions and Memory

Goal: maintain conversation state cleanly.

Common sessions:

- `SQLiteSession`
- `RedisSession` (extension)
- `SQLAlchemySession` (extension)
- `OpenAIConversationsSession`

```python
import asyncio
from agents import Agent, Runner, SQLiteSession

async def main():
    agent = Agent(name="Assistant", instructions="Reply in one short paragraph.")
    session = SQLiteSession("user_123")

    r1 = await Runner.run(agent, "I am planning a trip to Japan.", session=session)
    print(r1.final_output)

    r2 = await Runner.run(agent, "What places did I mention?", session=session)
    print(r2.final_output)

asyncio.run(main())
```

Advanced controls:

- `SessionSettings(limit=N)` to limit retrieved history
- `RunConfig.session_input_callback` for custom history filtering

## Level 6 - Multi-Agent Systems

Goal: split responsibilities and scale quality.

Two patterns:

- Handoffs: control transfers to specialist agent
- Agents-as-tools: central orchestrator remains in control

Handoff example:

```python
from agents import Agent

billing = Agent(name="Billing", instructions="Handle billing queries.")
tech = Agent(name="Technical", instructions="Handle technical issues.")

triage = Agent(
    name="Triage",
    instructions="Route to the right specialist.",
    handoffs=[billing, tech]
)
```

When to use:

- Handoffs for conversational ownership transfer
- Agents-as-tools for deterministic orchestrators

## Level 7 - Guardrails and Safety

Goal: constrain unsafe or off-policy behavior.

Guardrail types:

- Input guardrails: validate user input before/while run starts
- Output guardrails: validate final answer after completion
- Tool guardrails: validate function tool calls pre/post execution

Key details:

- Input guardrails support `run_in_parallel=True` (default) or blocking mode (`False`)
- Output guardrails run after completion and can raise `OutputGuardrailTripwireTriggered`

## Level 8 - Human in the Loop (Approvals)

Goal: require approval for sensitive actions.

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool(needs_approval=True)
async def cancel_order(order_id: int) -> str:
    return f"Cancelled order {order_id}"

agent = Agent(name="Support", instructions="Use tools when needed.", tools=[cancel_order])

async def main():
    result = await Runner.run(agent, "Cancel order 1234.")
    if result.interruptions:
        state = result.to_state()
        for interruption in result.interruptions:
            state.approve(interruption)  # or state.reject(interruption)
        result = await Runner.run(agent, state)
    print(result.final_output)

asyncio.run(main())
```

Also supported by:

- `Agent.as_tool(..., needs_approval=...)`
- `ShellTool`, `ApplyPatchTool`
- MCP servers and hosted MCP with approval config

## Level 9 - Streaming, Tracing, and Usage

Goal: production observability.

Streaming:

- Use `Runner.run_streamed(...)`
- Iterate `result.stream_events()`
- Event layers:
- raw response events (token-level deltas)
- run item events (tool call, output item, message item)
- agent-updated events

Tracing:

- Enabled by default
- Disable globally with `OPENAI_AGENTS_DISABLE_TRACING=1`
- Disable per run with `RunConfig(tracing_disabled=True)`

Usage metrics:

- `result.context_wrapper.usage`
- Includes request count + token totals
- Per-request data in `request_usage_entries`

## Level 10 - Models and Performance Tuning

Goal: optimize cost, latency, and quality.

Current docs note:

- Default model: `gpt-4.1`
- Recommended when available: `gpt-5.2`

Set model at:

- Agent level: `Agent(model="...")`
- Run level: `RunConfig(model="...")`
- Environment level: `OPENAI_DEFAULT_MODEL=...`

For GPT-5.x:

- SDK applies default `ModelSettings`
- For lower latency, docs recommend `reasoning.effort="none"` with `gpt-5.2` in many interactive cases

Non-OpenAI providers:

- Use LiteLLM integration: `pip install "openai-agents[litellm]"`

## Level 11 - MCP Integration

Goal: connect external tool ecosystems.

Supported MCP options:

- `HostedMCPTool`
- `MCPServerStreamableHttp`
- `MCPServerSse` (SSE noted as deprecated by MCP project for new integrations)
- `MCPServerStdio`

MCP best practices:

- Use approval policies (`require_approval`) for risky tools
- Cache tool listings where useful
- Prefer Streamable HTTP or stdio for new builds

## Level 12 - Realtime and Voice Agents

Goal: build low-latency voice/live systems.

Realtime:

- `RealtimeAgent`, `RealtimeRunner`
- Persistent session over websocket model layer
- Handles tools, handoffs, and output guardrails in realtime workflow

Voice:

- Build pipelines with STT -> agent/workflow -> TTS
- Use optional `voice` dependency group

## Production Checklist

- Define strong agent instructions and boundaries
- Use structured outputs where outputs feed code
- Add guardrails for safety-critical paths
- Add approvals (`needs_approval`) for destructive/external actions
- Persist sessions for user continuity
- Stream status to frontend for UX
- Enable tracing and usage monitoring
- Set `max_turns` and error handlers
- Add retries and fallback strategies
- Add evals and regression tests for prompt/tool behavior

## Copy-Paste Project Templates

### Template A: Minimal App (`app.py`)

```python
import asyncio
from agents import Agent, Runner

assistant = Agent(
    name="Assistant",
    instructions="You are helpful, concise, and factual."
)

async def main():
    result = await Runner.run(assistant, "Give me 3 ways to improve API reliability.")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Template B: Production Starter (`production_starter.py`)

```python
import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    SQLiteSession,
    function_tool,
)

class TriageOutput(BaseModel):
    category: str
    urgency: str
    action: str

@function_tool(needs_approval=True)
async def refund_order(order_id: str, reason: str) -> str:
    # Replace with real implementation
    return f"Refund request accepted for {order_id}: {reason}"

triage_agent = Agent(
    name="Triage",
    instructions=(
        "Classify support requests. Use tools only when appropriate. "
        "Be concise and policy-safe."
    ),
    tools=[refund_order],
    output_type=TriageOutput,
)

async def run_once(user_id: str, message: str):
    session = SQLiteSession(user_id)
    result = await Runner.run(triage_agent, message, session=session)

    while result.interruptions:
        state = result.to_state()
        # Replace this with UI/manual approval workflow.
        for interruption in result.interruptions:
            state.approve(interruption)
        result = await Runner.run(triage_agent, state)

    print(result.final_output)

async def main():
    await run_once("user_1", "I was double-charged for order A-123. Please refund.")

if __name__ == "__main__":
    asyncio.run(main())
```

## 2-Week Learning Plan

1. Day 1-2: Level 0-2
2. Day 3-4: Level 3-4
3. Day 5-6: Level 5-6
4. Day 7-8: Level 7-8
5. Day 9-10: Level 9-10
6. Day 11-12: Level 11
7. Day 13-14: Level 12 + capstone project

Capstone idea:

- Build a support platform with triage, specialist agents, tools, guardrails, approvals, memory, streaming UI, and tracing dashboard.

## Official References

- Intro: https://openai.github.io/openai-agents-python/
- Quickstart: https://openai.github.io/openai-agents-python/quickstart/
- Agents: https://openai.github.io/openai-agents-python/agents/
- Running agents: https://openai.github.io/openai-agents-python/running_agents/
- Tools: https://openai.github.io/openai-agents-python/tools/
- Sessions: https://openai.github.io/openai-agents-python/sessions/
- Handoffs: https://openai.github.io/openai-agents-python/handoffs/
- Multi-agent orchestration: https://openai.github.io/openai-agents-python/multi_agent/
- Guardrails: https://openai.github.io/openai-agents-python/guardrails/
- Human-in-the-loop: https://openai.github.io/openai-agents-python/human_in_the_loop/
- Streaming: https://openai.github.io/openai-agents-python/streaming/
- Tracing: https://openai.github.io/openai-agents-python/tracing/
- Usage: https://openai.github.io/openai-agents-python/usage/
- Models: https://openai.github.io/openai-agents-python/models/
- LiteLLM: https://openai.github.io/openai-agents-python/models/litellm/
- MCP: https://openai.github.io/openai-agents-python/mcp/
- Realtime quickstart: https://openai.github.io/openai-agents-python/realtime/quickstart/
- Voice quickstart: https://openai.github.io/openai-agents-python/voice/quickstart/
