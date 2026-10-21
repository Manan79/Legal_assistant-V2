import os
import sys
import asyncio

project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from Legal_graph.Agent.react_agent import main_react_agent
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uvicorn

app = FastAPI(
    title="AI Legal Assistant API",
    description="FastAPI wrapper for LangGraph legal assistant workflow",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = os.path.join(project_root, "Legal_graph", "frontend")

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_ui():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/api", tags=["Root"])
    async def api_root():
        """API Information endpoint"""
        return {
            "name": "AI Legal Assistant API",
            "version": "2.0.0",
            "endpoints": {
                "POST /legal_assistant": "Process legal query",
                "GET /health": "Health check",
                "GET /docs": "API documentation",
                "GET /": "Web UI"
            }
        }
else:
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint"""
        return {
            "name": "AI Legal Assistant API",
            "version": "2.0.0",
            "endpoints": {
                "POST /legal_assistant": "Process legal query",
                "GET /health": "Health check",
                "GET /docs": "API documentation"
            }
        }

@app.get("/health")
def health():
    return "All Ok"


class LegalQueryRequest(BaseModel):
    """Request model for legal queries"""
    query: str = Field(..., min_length=1, description="Your legal query or question")
    thread_id: Optional[str] = Field(None, description="Conversation thread ID for checkpointer memory")


@app.post("/legal_assistant", tags=["Legal Assistant"])
async def legal_assistant(request: LegalQueryRequest):
    response = await main_react_agent(request.query, request.thread_id)
    # print(response)
    return {
            "status": "success",
            "query": request.query,
            "response": response['answer'],
            "retrived context": response['context'],
            "timestamp": datetime.now().isoformat()
        }



if __name__ == "__main__":
    uvicorn.run(
        app="Legal_graph.Backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
