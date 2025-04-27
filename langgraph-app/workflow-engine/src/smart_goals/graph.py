from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, AnyMessage
from langgraph.types import Command, interrupt
from typing import Annotated, TypedDict, List, Dict, Sequence, Literal
from dataclasses import dataclass, field
from smart_goals.tools import get_user_details_tool
@dataclass
class AgentState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )

ANALYZE_USER_PROMPT = "Analyze the user's input and generate a list of 3 smart goals."
USER_DETAILS_PROMPT = "Find user deatails based on the user's name using tools. if user is not found, say that they are not found. otherwise return the user's role."
llm = ChatOpenAI(model="gpt-4o-mini")
class SmartGoalsGraph():
    workflow: StateGraph
    def __init__(self) -> None:
        self.workflow = StateGraph(AgentState)

    def create_analyze_user_agent(self):
        agent = create_react_agent(model=llm, prompt=ANALYZE_USER_PROMPT, tools=[])
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
        result = self.create_user_details_agent().invoke({"messages": state.messages})
        role = result["messages"][-1].content
        if role == "NOT_FOUND":
            message = AIMessage(content="User not found")
            return Command(goto="human_node", update={"messages": state.messages + [message]})
        message = AIMessage(content="Users role is: " + role)
        return Command(goto="analyze_user", update={"messages": state.messages + [message]})
        

    def human_node(self, state: AgentState) -> Command[Literal["analyze_user"]]:
        response = interrupt({"message": "What is user role ?"}) 
        message = HumanMessage(content="Users role is: " + response["role"])
        return Command(goto="analyze_user", update={"messages": state.messages + [message]}) 

    def compile(self) -> StateGraph:
        self.workflow.add_node("user_details", self.user_details_node)
        self.workflow.add_node("human_node", self.human_node)
        self.workflow.add_node("analyze_user", self.analyze_user_node)
        self.workflow.set_entry_point("user_details")
        return self.workflow.compile()

workflow = SmartGoalsGraph()
graph = workflow.compile()

# --- Example usage ---
# graph.invoke({"input":{"messages":[]},"output":{"messages":[]},"agent":{"messages":[]},"messages":[]})
