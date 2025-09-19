from datetime import datetime
from agents import Agent, RunContextWrapper , Runner , AsyncOpenAI, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff 
from agents.run import RunConfig
from agents.extensions import handoff_filters
import os
from dotenv import load_dotenv
from pydantic import BaseModel


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





# Create a pydantic model for the handoff input
class EscalationAgent(BaseModel):
    name: str
    instructions: str


#create a function for on_handoff example
def on_handoff_Agent_data(ctx: RunContextWrapper[None], agent: Agent ):
    print(f"Handoff to {agent.name} with instructions: {agent.instructions}")



# Create a function to determine if urdu agent is available
def is_urdu_agent_available(ctx: RunContextWrapper[None], agent: Agent[None]) -> bool:
    current_hour = datetime.now().hour
    # Return karega True agar 9 AM aur 5 PM ke beech ho, warna False
    return 9 <= current_hour < 17


#handsoff practise 
# Create the math agent with the model and config
math_agent = Agent(
    name="Math Agent",
    instructions="You are a helpful assistant that can solve math problems.",
    model= model,
)



# Create the urdu agent with the model and config
urdu_agent = Agent(
    name= "Urdu agent",
    instructions =" You are an Helpful assistant that can solve queries in urdu",
    model=model,
)



#Create the agent with the model and config
agent: Agent = Agent(
    name="Assistant",
    instructions=(
        "You are a helpful teacher. "
        "If the question involves mathematics, call the `Math Agent` via handoff."
    ),
    handoffs=[math_agent, 
        handoff(urdu_agent,
                tool_name_override="Urdu",
                tool_description_override="Use this tool to answer questions in Urdu.", 
                on_handoff=on_handoff_Agent_data,
                input_type=EscalationAgent,
                input_filter=handoff_filters.remove_all_tools,
                is_enabled=is_urdu_agent_available
        )
    ],
 
)


# Result of the run
result = Runner.run_sync(
    agent,
    "What is urdu?",
    run_config=config,
)


# Print the result of the run
print(result.final_output)