from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import ToolNode, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from typing import Annotated, TypedDict, List, Dict, Sequence
from dataclasses import dataclass, field

@dataclass
class AgentState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )

ANALYZE_USER_PROMPT = "Analyze the user's input and generate a list of 3 smart goals."

class SmartGoalsGraph():
    workflow: StateGraph
    def __init__(self) -> None:
        self.workflow = StateGraph(AgentState)

    def create_analyze_user_agent(self):
        agent = create_react_agent(model=ChatOpenAI(model="gpt-4o-mini"), prompt=ANALYZE_USER_PROMPT, tools=[])
        return agent

    def call_model(self, state: AgentState) -> AnyMessage:
        result = self.create_analyze_user_agent().invoke({"messages": state.messages})
        return {"messages":  [result["messages"][-1]]}

    def compile(self) -> StateGraph:
        self.workflow.add_node("analyze_user", self.call_model)
        self.workflow.add_edge(START, "analyze_user")
        self.workflow.add_edge("analyze_user", END)
        return self.workflow.compile()

workflow = SmartGoalsGraph()
graph = workflow.compile()

# --- Example usage ---
# graph.invoke({"input":{"messages":[]},"output":{"messages":[]},"agent":{"messages":[]},"messages":[]})
