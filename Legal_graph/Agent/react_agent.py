from langchain.agents import create_agent
from langchain.tools import tool
from models import openai_model, openrouter_model
from Prompts import System_prompt


agent = create_agent(
    model=openai_model(),
    system_prompt=System_prompt
)
