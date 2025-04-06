# graph.py
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dataclasses import dataclass, field
from typing import Sequence, Literal, TypedDict, Optional, Dict, Any

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage 
from langgraph.graph import add_messages, StateGraph, START, END
from typing_extensions import Annotated
from service_now_sentiment.prompts import (
    SERVICE_NOW_SYSTEM_PROMPT, 
    SENTIMENT_ANALYSIS_PROMPT, 
    SUMMARY_GENERATION_PROMPT,
    OLLAMA_AGENT_PROMPT
)

model = ChatOpenAI(model="gpt-4o-mini")
ollama_model = ChatOllama(model="phi3ft") 

@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )

# Function to extract the last message from ServiceNow agent for Ollama processing
async def sentiment_analysis_node(state: InputState) -> InputState:

     # Create the Ollama agent for local processing

    messages = [AIMessage(content=OLLAMA_AGENT_PROMPT)] + [state.messages[-1]]
   
    response = await ollama_model.ainvoke(messages)
    state.messages.append(response)
    return state

@asynccontextmanager
async def make_graph():
    async with MultiServerMCPClient(
        {
            "servicenow": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8090/sse",
                "transport": "sse",
            }
        }
    ) as client:
        # Create the ServiceNow agent with MCP tools
        servicenow_agent = create_react_agent(model, prompt=SERVICE_NOW_SYSTEM_PROMPT, tools=client.get_tools())
        
       

        # Set up the workflow
        workflow = StateGraph(InputState)
        
        # Add nodes to the workflow
        workflow.add_node("servicenow_agent", servicenow_agent)
        workflow.add_node("sentiment_analysis_node", sentiment_analysis_node)

        # Create a sequential flow: START -> ServiceNow -> extract_last_message -> Ollama -> END
        workflow.add_edge(START, "servicenow_agent")
        
        # Route from ServiceNow to extract_last_message, then to Ollama
        workflow.add_edge("servicenow_agent", "sentiment_analysis_node")
        workflow.add_edge("sentiment_analysis_node", END)

        graph = workflow.compile()

        yield graph