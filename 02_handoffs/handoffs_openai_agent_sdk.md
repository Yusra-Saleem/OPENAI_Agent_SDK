# Handoffs in OpenAI Agent SDK

This document provides a comprehensive, step-by-step guide to
understanding and implementing **Handoffs** within the OpenAI Agent SDK.
It covers the core concepts, practical implementation, and real-world
application of this powerful feature.

### 1. Handoffs: What and Why?

**Handoffs** allow a specialized agent to take over a task from another
agent. This is a fundamental concept for building complex and efficient
multi-agent systems. Instead of having a single agent handle all types
of queries, we can create a system of specialized agents, each an expert
in a specific domain.

**Logical Principle:** This approach follows the "Divide and Conquer"
strategy, where complex problems are broken down into smaller,
manageable sub-problems, and each sub-problem is assigned to a dedicated
expert. This ensures that the system provides more accurate and faster
responses.

**Example:** In a customer support system, a **Triage Agent** can direct
a user's request to a **Billing Agent** for billing queries, a **Refund
Agent** for refund issues, or an **Order Agent** for order status
updates.

### 2. Handoffs as "Tools"

To an **LLM (Large Language Model)**, a handoff is represented as a
**tool**. The LLM uses these tools to decide the next action based on
the user's input. For example, a handoff to an agent named "Refund
Agent" would be represented as a tool called `transfer_to_refund_agent`.

**Logical Principle:** This design enables the LLM to make intelligent,
context-aware decisions. By exposing handoffs as tools, we empower the
LLM to act as a smart orchestrator, autonomously selecting the most
appropriate agent for a given task, much like a human would consult a
specialist for a specific problem.

### 3. Creating a Handoff (Basic Usage)

Creating a handoff is straightforward. You can add another `Agent`
object directly to the `handoffs` list of a new agent, or use the
explicit `handoff()` function for more control.

``` python
from agents import Agent, handoff

# Specialized agents
billing_agent = Agent(name="Billing agent")
refund_agent = Agent(name="Refund agent")

# Triage agent with handoffs
triage_agent = Agent(
    name="Triage agent",
    handoffs=[billing_agent, handoff(refund_agent)]
)
```

**Explanation:**

-   **Direct Agent (`billing_agent`)**: The SDK automatically creates a
    handoff tool with a default name (`transfer_to_billing_agent`). This
    is simple but offers no customization.
-   **`handoff()` function (`handoff(refund_agent)`)**: This is the
    recommended approach as it provides a customizable way to define a
    handoff, which is crucial for advanced use cases.

------------------------------------------------------------------------

### 4. Customizing Handoffs

The `handoff()` function comes with several powerful parameters for
detailed customization.

#### a. `tool_name_override` and `tool_description_override`

These parameters allow you to override the default tool name and
description. A clear name and a detailed description help the LLM make
better decisions.

``` python
from agents import Agent, handoff

refund_agent = Agent(name="Refund agent")

triage_agent = Agent(
    name="Triage agent",
    handoffs=[
        handoff(
            agent=refund_agent,
            tool_name_override="process_refunds",
            tool_description_override="Use this tool to initiate or check the status of a user's refund request."
        )
    ]
)
```

#### b. `on_handoff` and `input_type`

-   **`on_handoff`**: A callback function that executes *before* the
    handoff occurs. This is useful for pre-handoff tasks like logging,
    data fetching, or database updates.
-   **`input_type`**: Allows the LLM to provide structured data to the
    next agent. This is defined using a Pydantic `BaseModel`.

``` python
from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper

class EscalationData(BaseModel):
    reason: str

async def on_handoff_to_escalation(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

escalation_agent = Agent(name="Escalation agent")

handoff_obj = handoff(
    agent=escalation_agent,
    on_handoff=on_handoff_to_escalation,
    input_type=EscalationData
)
```

#### c. `input_filter`

By default, the new agent receives the entire conversation history. An
**`input_filter`** is a function that modifies this history, for
example, by removing irrelevant messages or previous tool calls. This
keeps the context clean for the new agent.

``` python
from agents import Agent, handoff
from agents.extensions import handoff_filters

faq_agent = Agent(name="FAQ agent")

handoff_obj = handoff(
    agent=faq_agent,
    input_filter=handoff_filters.remove_all_tools,
)
```

#### d. `is_enabled`

This parameter allows for dynamic enabling or disabling of a handoff. It
can be a boolean or a callable function that returns a boolean, useful
for scenarios like time-based availability.

``` python
import datetime
from agents import Agent, handoff, RunContextWrapper

billing_agent = Agent(name="Billing agent")

def is_billing_agent_available(ctx: RunContextWrapper[None], agent: Agent[None]) -> bool:
    current_hour = datetime.datetime.now().hour
    return 9 <= current_hour < 17

triage_agent = Agent(
    name="Triage agent",
    handoffs=[
        handoff(
            agent=billing_agent,
            is_enabled=is_billing_agent_available
        )
    ]
)
```

------------------------------------------------------------------------

### 5. Design Patterns with Handoffs

Handoffs enable powerful design patterns for building robust multi-agent
systems.

#### a. The Router Pattern (or Triage Agent Pattern)

A central **Router Agent** receives all incoming requests and hands them
off to the appropriate specialized agent. This pattern simplifies system
design and improves efficiency.

#### b. The Hierarchical Pattern

In this pattern, agents are organized in a hierarchy. An agent can hand
off a task to a more specialized agent within its domain. For example, a
"Customer Support Agent" could hand off a technical query to a "Senior
Support Agent." This allows for progressive specialization and efficient
problem-solving.

### 6. Real-World Applications

-   **Customer Support Automation:** A Triage Agent routes user queries
    to specialized agents for billing, order status, or technical
    support.
-   **Banking Chatbot:** A central agent handles basic queries but hands
    off complex requests for loan applications or human assistance to
    specialized agents.
-   **Internal Knowledge Management:** A "General Agent" directs
    employee queries to specialized agents who are experts on topics
    like HR policies, IT support, or project management.

By combining these concepts, you can build a highly organized,
efficient, and scalable system using the power of Handoffs.
