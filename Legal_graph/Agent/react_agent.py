from langchain.agents import create_agent
from langchain.tools import tool
from models import openai_model


agent = create_agent(
    model=openai_model(),
    
)
