from datetime import date
from langgraph.graph import StateGraph, END, add_messages
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langgraph.types import Command, interrupt
from typing import Annotated, Sequence, Literal
from dataclasses import dataclass, field
from smart_goals.tools import get_user_details_tool
from smart_goals.prompts import GOAL_PROMPT, USER_DETAILS_PROMPT
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

@dataclass
class AgentState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )


llm = ChatOpenAI(model="gpt-4o-mini")
class SmartGoalsGraph():
    workflow: StateGraph
    def __init__(self) -> None:
        self.workflow = StateGraph(AgentState)

    def create_analyze_user_agent(self):
        prompt = GOAL_PROMPT.format(date=date.today())
        agent = create_react_agent(model=llm, prompt=prompt, tools=[])
        return agent

    def create_user_details_agent(self):
        tools = [get_user_details_tool]
        llm_with_tools = llm.bind_tools(tools)
        agent = create_react_agent(model=llm_with_tools, prompt=USER_DETAILS_PROMPT, tools=tools)
        return agent

    def analyze_user_node(self, state: AgentState) -> Command[Literal[END]]:
        result = self.create_analyze_user_agent().invoke({"messages": state.messages})
        message = result["messages"][-1]
        return Command(goto=END, update={"messages": state.messages + [message]}) 

    def user_details_node(self, state: AgentState) -> Command[Literal["analyze_user", "human_node"]]:
        # if len(state.messages) > 1:
        #     return Command(goto="analyze_user", update={"messages": state.messages})

        result = self.create_user_details_agent().invoke({"messages": state.messages})
        role = result["messages"][-1].content
        if role == "NOT_FOUND":
            message = AIMessage(content="User not found")
            
            return Command(goto="human_node", update={"messages": state.messages + [message]})
        message = AIMessage(content="Users role is: " + role)
        return Command(goto="analyze_user", update={"messages": state.messages + [message]})
        

    def human_node(self, state: AgentState) -> Command[Literal["analyze_user", END]]:
        response = interrupt({"message": "What is user role ?"}) 
        role = response["role"]
        if not role:
            aimssage = AIMessage(content="What is user role ?")
            message = HumanMessage(content="User not found. Stoping generating goals")
            return Command(goto=END, update={"messages": state.messages +[aimssage] + [message]})
        message = HumanMessage(content="Users role is: " + response["role"])
        return Command(goto="analyze_user", update={"messages": state.messages + [message]}) 

    def compile(self) -> StateGraph:
        conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
        memory = SqliteSaver(conn)
        self.workflow.add_node("user_details", self.user_details_node)
        self.workflow.add_node("human_node", self.human_node)
        self.workflow.add_node("analyze_user", self.analyze_user_node)
        self.workflow.set_entry_point("user_details")
        return self.workflow.compile(checkpointer=memory)

def make_graph():
    workflow = SmartGoalsGraph()
    graph = workflow.compile()
    return graph

    

# --- Example usage ---
# graph.invoke({"input":{"messages":[]},"output":{"messages":[]},"agent":{"messages":[]},"messages":[]})
