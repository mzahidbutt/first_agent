import os

import asyncio

from dotenv import load_dotenv, find_dotenv

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool

_: bool = load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Tracing disabled
set_tracing_disabled(disabled=True)

# Client Setup for Connecting to Gemini
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Initialize model
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def add(a: int, b: int) -> int:
    """Adds two integers."""
    print(f"Adding {a} and {b}")
    return a + b

@function_tool
def subtract(a: int, b: int) -> int:
    """Subtracts two integers."""
    print(f"Subtracting {b} from {a}")
    return a - b

math_agent: Agent = Agent(
    name="Alex, The Math Agent",
    instructions="An agent that answers questions about math and its applications in AI.",
     model=model,
     tools=[add, subtract]
)

async def call_agent():
    result = await Runner.run(starting_agent=math_agent,input="what is 4 + 2. and what is 5 - 3 is ?")
   # result = Runner.run_sync(starting_agent=math_agent,input="shy learn math?")
    print(result.final_output)

asyncio.run(call_agent())

#print("\nCALLING AGENT\n")
#print(result.final_output)