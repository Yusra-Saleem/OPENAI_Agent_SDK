from agents import Agent , Runner , AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging 
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
    model="gemini-2.0-flash",
)


# Set config for the run
config = RunConfig(
    model=model,
    model_provider=my_client,
    tracing_disabled=True,
)


#Create the agent with the model and config
agent: Agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant. "
        
    ),
    model=model,
)


# Result of the run
result = Runner.run_sync(
    agent,
    "What is the capital of Pakistan?",
    run_config=config,
)


# Print the result of the run
print(result.final_output)

