from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered , OpenAIChatCompletionsModel, OutputGuardrailTripwireTriggered, RunContextWrapper , Runner , AsyncOpenAI, TResponseInputItem, input_guardrail, output_guardrail
from agents.run import RunConfig
import os
from dotenv import load_dotenv
from pydantic import BaseModel


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
    tracing_disabled=True,
)

#input guardrail

class Datatype(BaseModel):
    programming_language: bool
    reasoning: str


input_guardrail_agent: Agent = Agent(
    name="GuardrailAgent",
    instructions="check if the user question is about programming language",
    output_type=Datatype,
    model=model, 
)


@input_guardrail
async def check_programming_language(ctx: RunContextWrapper[None], agent:Agent , user_input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    
    result = await Runner.run(input_guardrail_agent, user_input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.programming_language
    )
    

input_agent: Agent = Agent(
    name="Assistant",
    instructions="you are a helpful assistant",
    input_guardrails=[check_programming_language], 
)


try:
    result = Runner.run_sync(
        input_agent,
        "hello what is python",
        run_config=config,
    )

    print(result.final_output)

except InputGuardrailTripwireTriggered as e:
  
    print(f"Tripwire triggered: \n {e}")




#--------------------------------------------------------------------

#output guardrails

class Message(BaseModel):
    response : str


class Programming_Language_Output(BaseModel):
    programming_language: bool
    reasoning: str

output_guardrail_agent: Agent = Agent(
    name="OutputGuardrailAgent",
    instructions="Determine if the user's question is about programming languages.",
    output_type=Programming_Language_Output,
    model=model, 
)

@output_guardrail
async def ensure_programming_language(ctx: RunContextWrapper[None], agent: Agent, output: Message) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.programming_language
    )

output_agent: Agent = Agent(
    name="Assistant",
    instructions="you are a helpful assistant that helps to answer questions about the programming language.",
    output_guardrails=[ensure_programming_language], 
    output_type=Message,
)


try:
    result = Runner.run_sync(
        output_agent,
        "Hello!",
        run_config=config,
    )

    print(result.final_output)

except OutputGuardrailTripwireTriggered as e:
    print(f"output Tripwire triggered: \n {e}")
