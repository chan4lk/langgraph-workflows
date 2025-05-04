# graph.py
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dataclasses import dataclass, field
from typing import Sequence, Literal, TypedDict, Optional, Dict, Any, List

from langchain_core.messages import AnyMessage, HumanMessage, AIMessage 
from langgraph.graph import add_messages, StateGraph, START, END
from typing_extensions import Annotated
from service_now_sentiment.prompts import (
    SERVICE_NOW_SYSTEM_PROMPT, 
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

@dataclass
class OutputState:
    ticketText: List[str]

# Function to extract the last message from ServiceNow agent for Ollama processing
async def format_ollama_input_node(state: InputState) -> InputState:

     # Create the Ollama agent for local processing
    print(f"messages {state.messages[-1]}")
    messages = [AIMessage(content=SUMMARY_GENERATION_PROMPT)] + [state.messages[-1]]
    model_structured_output = model.with_structured_output(OutputState)
    response = await model_structured_output.ainvoke(messages)
    print(f"response {response}")
    ticketsDetails: List[str] = response["ticketText"]
    singleString = ' '.join(ticketsDetails)
    message = AIMessage(content=singleString)
    state.messages.append(message)
    return state

# Function to extract the last message from ServiceNow agent for Ollama processing
async def sentiment_analysis_node(state: InputState) -> InputState:

     # Create the Ollama agent for local processing
    
    message = state.messages[-1]
    prompt = OLLAMA_AGENT_PROMPT.format(text=message.content)
    messages = [AIMessage(content=prompt)]
    
    response = await ollama_model.ainvoke(messages)
    state.messages.append(response)
    return state

@asynccontextmanager
async def make_graph():
    try:
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
            workflow.add_node("format_ollama_input_node", format_ollama_input_node)

            # Create a sequential flow: START -> ServiceNow -> extract_last_message -> Ollama -> END
            workflow.add_edge(START, "servicenow_agent")
            
            # Route from ServiceNow to extract_last_message, then to Ollama
            workflow.add_edge("servicenow_agent", "format_ollama_input_node")
            workflow.add_edge("format_ollama_input_node", "sentiment_analysis_node")
            workflow.add_edge("sentiment_analysis_node", END)

            graph = workflow.compile()

            yield graph
    except Exception as e:
        print(e)
        yield None