from agents import Agent, ModelSettings , Runner , AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, function_tool , handoffs
from agents.run import RunConfig
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
enable_verbose_stdout_logging()


# Set up the Gemini key
gemini_key = os.getenv("GEMINI_API_KEY")


# Check if the GEMINI_API_KEY is set
if not gemini_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


# Set up the OpenAI client with Gemini API key and base URL
my_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# Set model to use
model = OpenAIChatCompletionsModel(
    openai_client=my_client,
    #gpt-5 model
    model="gpt-5",
)


# Set config for the run
config = RunConfig(
    model=model,
    model_provider=my_client,
    tracing_disabled=True,
)


@function_tool
def get_poetry_about(topic: str) -> str:
    """Generate a poetry about the given topic."""
    return f"This is a poetry about {topic}."

@function_tool
def get_summary(topic) -> str:
    """Generate a summary of the given text."""
    return f"This is a summary of the text about {topic}."

#Create the agent with the model and config
agent: Agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant.if the user asks you to create a poetry, use the get_poetry_about tool.and if the user asks you to summarize a text, use the get_summary tool."
        
    ),
    model=model,
    tools=[get_poetry_about, get_summary],
    model_settings=ModelSettings(temperature=0.9, max_tokens=500,tool_choice="required", parallel_tool_calls=True ),
)


# Result of the run
result = Runner.run_sync(
    agent,
    "create a poetry about the sea and summarize it",
    run_config=config,
)


# Print the result of the run
print(result.final_output)