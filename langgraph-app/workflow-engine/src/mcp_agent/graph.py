# graph.py
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from dataclasses import dataclass, field
from typing import Sequence

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages, StateGraph, START, END
from typing_extensions import Annotated

model = ChatOpenAI(model="gpt-4o-mini") 

@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )

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
            "postgresql://elb:postgres@host.docker.internal:5432/elb"],
            "transport":"stdio"
        }
        }
    ) as client:
        agent = create_react_agent(model,prompt="Alway query the db schema first. then answer users query", tools=client.get_tools())

        sub_graph_workflow = StateGraph(InputState)
        sub_graph_workflow.add_node("executor", agent)
        sub_graph_workflow.add_edge(START, "executor")
        sub_graph_workflow.add_edge("executor", END)
        sub_graph = sub_graph_workflow.compile()

        yield sub_graph