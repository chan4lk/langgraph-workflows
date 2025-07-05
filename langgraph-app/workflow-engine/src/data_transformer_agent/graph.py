from langchain_openai import ChatOpenAI
from dataclasses import dataclass, field
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_core.messages import AnyMessage, AIMessage
from typing import Sequence
from typing_extensions import Annotated, Dict
from ai_data_science_team.agents import DataLoaderToolsAgent, DataCleaningAgent, DataWranglingAgent
import os
import pandas as pd
from datetime import datetime

@dataclass
class State:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    artifact: Dict = field(
        default_factory=dict
    )
    cleaned_data: Dict = field(
        default_factory=dict
    )
    wrangled_data: Dict = field(
        default_factory=dict
    )

llm = ChatOpenAI(model="gpt-4o-mini")
LOG      = True
LOG_PATH = os.path.join(os.getcwd(), "logs/")

# Make a data loader agent
data_loader_agent = DataLoaderToolsAgent(
    llm, 
    invoke_react_agent_kwargs={"recursion_limit": 10}, 
)

data_cleaning_agent = DataCleaningAgent(
    llm,
    log=LOG,
    log_path=LOG_PATH,
)

data_wrangling_agent = DataWranglingAgent(
    model = llm, 
    log=LOG, 
    log_path=LOG_PATH
)

def data_loader_node(state: State):
   data_loader_agent.invoke_agent(state.messages[-1].content)
   response = data_loader_agent.get_ai_message()
   artifact = data_loader_agent.get_artifacts()
   return { "messages": state.messages + [AIMessage(content=response)], "artifact": artifact }

def data_cleaning_node(state: State):
   dict_data = state.artifact
   df = pd.DataFrame(dict_data)
   today = datetime.now().strftime("%Y-%m-%d")
   data_cleaning_agent.invoke_agent(
    data_raw=df,
    user_instructions="Remove rows where the date is is not 11/12/2024s. Don't remove outliers when cleaning the data.", 
    max_retries=3, 
    retry_count=0
   )
   response = data_cleaning_agent.get_response()
   cleaned_data = data_cleaning_agent.get_data_cleaned()
   return { "messages": state.messages + [AIMessage(content="Data cleaned successfully")], "cleaned_data": cleaned_data.to_dict() }

def data_wrangling_node(state: State):
   dict_data = state.cleaned_data
   df = pd.DataFrame(dict_data)
   data_wrangling_agent.invoke_agent(
    data_raw=[df],
    user_instructions="Group the data frames on the ServiceName column. Keep only the 'ServiceName', 'Quantity', 'Cost' columns.",
    max_retries=3,
    retry_count=0
   ) 
   response = data_wrangling_agent.get_response()
   wrangled_data = data_wrangling_agent.get_data_wrangled()
   return { "messages": state.messages + [AIMessage(content="Data wrangled successfully")], "wrangled_data": wrangled_data.to_dict() }

workflow = StateGraph(State)
workflow.add_node("data_loader", data_loader_node)
workflow.add_node("data_cleaning", data_cleaning_node)
workflow.add_node("data_wrangling", data_wrangling_node)

workflow.add_edge(START, "data_loader")
workflow.add_edge("data_loader", "data_cleaning")
workflow.add_edge("data_cleaning", "data_wrangling")
workflow.add_edge("data_wrangling", END)

graph = workflow.compile()
