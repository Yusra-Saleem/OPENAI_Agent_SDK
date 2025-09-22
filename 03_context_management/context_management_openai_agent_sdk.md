
# Context Management in OpenAI Agent SDK 

Context is a crucial concept in building intelligent AI agents. It's simply all the information the agent needs to perform a task correctly. In the OpenAI Agent SDK, context can be divided into two main categories: **local context** and **LLM context**. Understanding their differences and how they work together is key to building powerful agents.

-----

## 1. Local Context: The Agent's Private Data

Local context is data that is only available to your code, such as your tool functions and lifecycle hooks. The LLM itself **cannot see or access this data directly**. Think of it as the agent's private, behind-the-scenes information.

### How It Works

The SDK uses the **`RunContextWrapper`** class to manage local context.

1.  **Define Your Context**: First, you create a standard Python object to hold your data. A **dataclass** is a great choice for this because it's clean and easy to use. For example, we defined `UserInfo` to store a user's name and ID.

    ```python
    from dataclasses import dataclass

    @dataclass
    class UserInfo:
        name: str
        uid: int
    ```

2.  **Pass the Context**: When you start a run, you pass your context object to the `Runner.run` or `Runner.run_sync` function using the `context` parameter.

    ```python
    user_info = UserInfo(name="Alice", uid="12345")
    result = await Runner.run(..., context=user_info)
    ```

3.  **Access in Tools**: Inside your tool functions, you can access this data via the `RunContextWrapper`. The wrapper acts as a container for your object. You use `wrapper.context` to get to your original data.

    ```python
    from agents import RunContextWrapper, function_tool

    @function_tool
    async def get_user_info(wrapper: RunContextWrapper[UserInfo]) -> str:
        # Get the user's name and age from their profile
        return f"Her name is {wrapper.context.name} and her age is 19 years old."
    ```

### Why It Works This Way

This design pattern separates the agent's logic from its data. The `RunContextWrapper` provides a **standardized interface** for all tools, regardless of the specific data they need. It also keeps your LLM's prompt clean and focused, preventing it from seeing data that is not relevant to its conversational task, like a user's internal database ID.

### **Important Note**

Every agent and tool function within a single `Runner.run` call **must use the same type of context**. For example, if your main agent uses `UserInfo`, all its tools must also expect a `UserInfo` object via the `RunContextWrapper`.

-----

## 2. Agent/LLM Context: The Conversation History

The LLM can only see information that is part of the **conversation history**. If you want the LLM to know something, you must put it into this history. There are several ways to do this.

### A. Instructions (System Prompt)

This is a set of initial instructions or a "system prompt" that you give to the agent at the beginning of a run. It helps define the agent's **persona** and its core rules.

  * **How to Use**: Pass a string to the `instructions` parameter when creating the `Agent` object.
  * **Purpose**: Use this for **static or fundamental information** that the LLM should remember throughout the entire conversation, like its role or tone.

### B. Function Tools

This is the most powerful method for providing **dynamic, on-demand** context. The LLM decides when it needs specific data and calls a tool to fetch it.

  * **How it Works**:
    1.  You provide a tool (like `get_user_info`) that fetches data from your local context.
    2.  The LLM's prompt includes a description of this tool, so it knows what the tool does.
    3.  When the user asks a question that requires the tool's data (e.g., "What is her name and age?"), the LLM decides to call the tool.
    4.  The tool runs, accesses the local context (`wrapper.context`), and returns a string with the relevant information.
    5.  This string is then added to the conversation history, and the LLM sees it.

This is why your recent code started working correctly: you included the tool, and the LLM used it to get the information it needed.

-----

## 3. Practical Example: My Sync Gemini Agent

You've built a complete, working example using the **sync** method. Here is the final, corrected code, with detailed comments explaining each part.

```python
# 1. Imports for sync functionality and Gemini configuration
from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool, OpenAIChatCompletionsModel, OpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Configure the sync OpenAI client for Gemini
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 3. Use the sync client with the correct Gemini model
model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash", # Use a valid, stable model name
)

config = RunConfig(
    model=model,
    tracing_disabled=True,
)

# 4. Define your local context data structure
@dataclass
class UserData:
    name: str
    age: int

# 5. Define a sync tool function with a type hint for the context
# The function will access the UserData via the wrapper.
@function_tool
def UserInfo(wrapper: RunContextWrapper[UserData]) -> str:
    \"\"\"get the user name and age from their profile\"\"\"
    return f"Her name is {wrapper.context.name} and her age is {wrapper.context.age} years old"

# 6. Main function to run the agent
def main():
    # 7. Define the agent and its instructions
    agent = Agent[UserData](
        "Assistant",
        "You should use the tool to get the user's information",
        tools=[UserInfo],
    )

    # 8. Run the agent in a synchronous manner
    result = Runner.run_sync(
        starting_agent=agent,
        input="what's her age and name?",
        context=UserData(name="Yusra", age=19),
        run_config=config,
    )

    print(result.final_output)

# 9. Start the program
if __name__ == "__main__":
    main()
```

### Logical Breakdown

  * **Line 1-10**: We import necessary libraries and set up the `sync` Gemini API client.
  * **Line 13-16**: The `UserData` dataclass defines the **local context**. This is the private data we want to pass to our tools.
  * **Line 18-22**: The `UserInfo` tool is where the magic happens. It's a sync function that takes the `RunContextWrapper[UserData]` as input. It then **reads from the local context** (`wrapper.context.name`, `wrapper.context.age`) and creates a string.
  * **Line 25-30**: The `Agent` is created.
      * `Agent[UserData]`: This **type hint** tells the SDK that this agent expects a `UserData` object for its context.
      * `instructions`: The LLM reads this and knows it has to use a tool to get information.
      * `tools=[UserInfo]`: We make the `UserInfo` tool **available to the LLM**.
  * **Line 33-37**: `Runner.run_sync` starts the process.
      * The `input` is the user's query.
      * `context=UserData(...)`: This is where we inject the **local context** into the run.
  * **Execution Flow**:
    1.  The LLM receives the prompt and the tool definition.
    2.  It sees the input "what's her age and name?".
    3.  Based on the instructions and the tool's description, it decides to **call the `UserInfo` tool**.
    4.  The SDK calls your `UserInfo` function and passes the `UserData` object inside the `RunContextWrapper`.
    5.  The function returns the string "Her name is Yusra and her age is 19 years old".
    6.  This string is added to the conversation history.
    7.  The LLM sees this new information and generates a complete final response.

This complete example demonstrates how local context and LLM context work together to create an intelligent and context-aware agent.
