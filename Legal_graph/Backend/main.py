import os
import sys
import asyncio

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from Legal_graph.Agent.react_agent import main_react_agent
from pydantic import BaseModel, Field
# from typing import Optional, Dict, Any
from datetime import datetime
import uvicorn

# app = FastAPI(
#     title="AI Legal Assistant API",
#     description="FastAPI wrapper for LangGraph legal assistant workflow",
#     version="2.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc"
# )
app = FastAPI()


class LegalQueryRequest(BaseModel):
    """Request model for legal queries"""
    query: str = Field(..., min_length=1, description="Your legal query or question")
    

@app.get("/health")
def health():
    return "All Ok"

@app.post("/legal_assistant", tags=["Legal Assistant"])
async def legal_assistant(request: LegalQueryRequest):
    response = await main_react_agent(request.query)
    return {
            "status": "success",
            "query": request.query,
            "response": response['answer'],
            # "retrived context": response.context,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=True,

    )
