import os

import asyncio

from dotenv import load_dotenv, find_dotenv

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

_: bool = load_dotenv(find_dotenv())

#gemini_api_key: str = os.getenv("GAMANI_API_KEY", "")

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Tracing disabled
#set_tracing_disabled(disabled=True)


# Client Setup for Connecting to Gemini
external_client:AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

#Initialize model
model:OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)


   
math_agent: Agent = Agent(
    name="MathAgent",
    instructions="An agent that answers questions about math and its applications in AI.",
     model=model
)

async def call_agent():
    result = await Runner.run(starting_agent=math_agent,input="Why learn math?")
   # result = Runner.run_sync(starting_agent=math_agent,input="shy learn math?")
    print(result.final_output)

asyncio.run(call_agent())

#print("\nCALLING AGENT\n")
#print(result.final_output)