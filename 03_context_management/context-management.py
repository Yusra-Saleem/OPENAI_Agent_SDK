from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool ,OpenAIChatCompletionsModel, AsyncOpenAI, enable_verbose_stdout_logging
from agents.run import RunConfig
from dotenv import load_dotenv
import os


enable_verbose_stdout_logging()
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(
    api_key = GEMINI_API_KEY,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client = client,
    model = "gemini-1.5-flash",
)

config = RunConfig(
    model = model,
    tracing_disabled=True,
)



@dataclass
class UserData:
    name:str
    age:int

@function_tool
def UserInfo(wrapper:RunContextWrapper[UserData])->str :
    """get the user name and age from their profile"""
    return f" Her name is {wrapper.context.name} and her age is {wrapper.context.age} years old"


agent =  Agent[UserData](

    "Assistant" , 
    "You should use the tool to get the user's information" ,
    tools= [UserInfo] ,
)

result = Runner.run_sync( agent , "what's her age and name?" ,context= UserData(name = "Yusra", age =19), run_config = config)

print(result.final_output)