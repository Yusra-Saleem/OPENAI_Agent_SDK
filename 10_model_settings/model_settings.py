from agents import (
    Agent,
    ModelSettings,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    enable_verbose_stdout_logging,
    function_tool,
)
from agents.run import RunConfig
import os
from dotenv import load_dotenv

load_dotenv()
enable_verbose_stdout_logging()





# 5) Define tools with correct type annotations
@function_tool
def get_poetry_about(topic: str) -> str:
    """Generate a poetry about the given topic."""
    return f"This is a poetry about {topic}.\n(Your tool generated text)"

@function_tool
def get_summary(text: str) -> str:
    """Generate a summary of the given text."""
    return f"This is a summary of the text about {text}."

# 6) Create the agent (include model, tools, settings)
agent: Agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant. "
        "If the user asks you to create poetry, call the get_poetry_about tool with a 'topic' argument. "
        "If the user asks to summarize text, call the get_summary tool with the full text to summarize."
    ),                  
    tools=[get_poetry_about, get_summary],
    model_settings=ModelSettings(
        temperature=0.9,
        max_tokens=500,
        tool_choice="required",          
        parallel_tool_calls=True,
    ),
)

# 7) Run the agent with RunConfig
result = Runner.run_sync(
    agent,
    "Please create a poetry about the sea and then give a short summary of that poetry.",
    
)

print("=== FINAL OUTPUT ===")
print(result.final_output)
