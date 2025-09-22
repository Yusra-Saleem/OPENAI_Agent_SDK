from agents import Agent , OpenAIChatCompletionsModel, RunContextWrapper , Runner , AsyncOpenAI, custom_span, enable_verbose_stdout_logging, function_tool, trace
from agents.run import RunConfig
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# enable_verbose_stdout_logging()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
 )    

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

config = RunConfig(
    model=model,
    model_provider=client,
    # tracing_disabled=False,
    # trace_include_sensitive_data=False
)


@function_tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b


@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b




english_agent :Agent = Agent(
    name="EnglishAgent",
    instructions="You are a helpful assistant that helps with English problems.",
)

math_agent :Agent = Agent(
    name="MathAgent",
    instructions="You are a helpful assistant that helps with math problems.if you need to add two numbers, use the tool",
    tools=[add, subtract],
)

agent :Agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that helps with math problems. if you need to do any math, hand off the request to the MathAgent. If you need to help with English, hand off the request to the EnglishAgent.",
    handoffs=[math_agent, english_agent],
)


res= Runner.run_sync( agent , "9+2?" , run_config=config)
print(res.final_output)



with trace("Math workflow"):
    print("\n---- First Run ---- \n" )

    res_1= Runner.run_sync( agent , "2+2?" , run_config=config)
    print(res_1)

    print("\n---- Second Run ---- \n" )

    res_2= Runner.run_sync( agent , f"{res_1.final_output} - 6?" , run_config=config)
    print(res_2.final_output)
    print(res_2.last_agent.name)

    with custom_span("English span"):
        print("\n---- custom span ---- \n" )

        res_3= Runner.run_sync( agent , f"what is the english word for {res_2.final_output}?" , run_config=config)
        print(res_3.final_output)
        print(res_3.last_agent.name)

