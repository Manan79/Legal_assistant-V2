from langchain.chat_models import init_chat_model



llm = init_chat_model(model='openai:gpt-4o-mini', temperature=0.0)
print(llm.invoke("Hii"))