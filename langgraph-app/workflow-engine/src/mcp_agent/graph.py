# graph.py
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini") 

@asynccontextmanager
async def make_graph():
    async with MultiServerMCPClient(
        {
         "postgres": {
            "command": "docker",
            "args": [
            "run", 
            "-i", 
            "--rm", 
            "mcp/postgres", 
            "postgresql://postgres:mysecretpassword@host.docker.internal:5432/kaya-ai-platform"],
            "transport":"stdio"
        },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        yield agent