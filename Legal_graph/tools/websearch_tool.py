from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

@tool("websearch")
def websearch(query):
    """Use this tool to search the web for the latest information on a topic."""
    print("-"*9, "Invoking Websearch" , "-"*9)
    print("Web Search Tool Called with query:", query)
    tool = TavilySearch(
        max_results=5,
        topic='general',
    )
    return tool.invoke({'query': query})
    
    # return {'retriever_docs' : tool.invoke({'query': query}) , 'tools_used': ['websearch']}

