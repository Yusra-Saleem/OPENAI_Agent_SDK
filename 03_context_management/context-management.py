from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI, enable_verbose_stdout_logging
from agents.run import RunConfig
from dotenv import load_dotenv
import os

# Enable verbose logging for debugging
enable_verbose_stdout_logging()

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini API
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the chat completions model using Gemini
model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

# Configure the run settings for the agent
config = RunConfig(
    model=model,
    tracing_disabled=True,
)





# Define a dataclass to hold user data
@dataclass
class UserData:
    name: str
    age: int

# Define a function tool to extract user info from context
@function_tool
def UserInfo(wrapper: RunContextWrapper[UserData]) -> str:
    """Get the user name and age from their profile."""
    return f" Her name is {wrapper.context.name} and her age is {wrapper.context.age} years old"

# Create an agent that uses the UserInfo tool
agent = Agent[UserData](
    "Assistant",
    "You should use the tool to get the user's information",
    tools=[UserInfo],
)

# Run the agent synchronously with example user data and a prompt
result = Runner.run_sync(
    agent,
    "what's her age and name?",
    context=UserData(name="Yusra", age=19),
    run_config=config
)

# Print the final output from the agent
print(result.final_output)