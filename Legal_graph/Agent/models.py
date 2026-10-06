from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
import os
load_dotenv()


def openai_model(model_name: str = 'gpt-5.4-mini') -> ChatOpenAI:
    endpoint = os.environ['Azure_OPENAI_Endpoint']
    api_key = os.environ['FOUNDRY_API_KEY']

    return ChatOpenAI(
        model=model_name,
        base_url=endpoint,
        api_key=api_key,
        use_responses_api=True,
        temperature=0.4,
    )


def openrouter_model(model_name: str = 'qwen/qwen3.5-9b') -> ChatOpenRouter:

    api_key = os.environ['OPENROUTER_API_KEY']

    return ChatOpenRouter(
        model=model_name,
        api_key=api_key,
        use_responses_api=True,
        temperature=0.4,
    )