
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel 
from agents.run import RunConfig
import os 
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()
# Set up the Gemini key
gemini_key = os.getenv("GEMINI_API_KEY")



# Check if the GEMINI_API_KEY is set
if not gemini_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


#set up the OpenAI client with Gemini API key and base URL

my_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# set model to use

model = OpenAIChatCompletionsModel(
    openai_client=my_client,
    model="gemini-2.0-flash",
)

# set config for the run

config = RunConfig(
    model=model,
    model_provider=my_client,
    tracing_disabled=True,
)

# create the agent with the model and config

agent : Agent = Agent(
    name="Open AI Agent SDK Agent",
    instructions="You are a teacher who helps student to learn open AI Agent SDK in dept with work flow , design patterns , best practices , architecture and implementation details.",
    model=model,
)

# result of the run
result = Runner.run_sync(
    agent ,
    "how many topics in open ai agent sdk python you know about in detail in dept and can teach me? only name like ",
    run_config=config,
)
# print the result of the run
print(result.final_output)





