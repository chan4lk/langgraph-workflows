from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode , create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from typing import Annotated, TypedDict, List, Dict

# --- Define the state of the graph ---
class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    mermaid_diagram: Annotated[str, "The mermaid diagram."]
    messages: Annotated[List, "The messages."]

# --- Create the tool for checking mermaid diagram syntax ---
@tool
def check_mermaid_syntax(diagram: str) -> str:
    """
    Checks the syntax of a Mermaid diagram.
    It uses mermaid-js to validate the syntax.
    """
    try:
        from mermaid import mermaidAPI
        mermaidAPI.initialize({"startOnLoad":False})
        mermaidAPI.parse(diagram)
        return "The Mermaid syntax is valid."
    except Exception as e:
        return f"Error: The Mermaid syntax is invalid. {str(e)}"

# --- Create the tool for fixing mermaid diagram syntax ---
@tool
def fix_mermaid_diagram(diagram: str) -> str:
    """
    Fixes a Mermaid diagram using an LLM.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that fixes Mermaid diagrams."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Here is the invalid Mermaid diagram : {diagram}"),
    ])
    llm = ChatOpenAI(model="gpt-4-1106-preview")
    chain = prompt | llm
    response = chain.invoke({"diagram":diagram,"messages":[]})
    return response.content

tools = [check_mermaid_syntax, fix_mermaid_diagram]
tool_executor = ToolNode(tools)

# --- Define agent ---

agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. You should use tools to fix the mermaid diagram."),
    MessagesPlaceholder(variable_name="messages"),
])
llm = ChatOpenAI(model="gpt-4-1106-preview")
agent = agent_prompt | llm

agent_executor = create_react_agent(llm, tools=tools)

# --- Define the node ---
def fix_mermaid_node(state: GraphState):
    """
    This is a node in the graph.
    """
    mermaid_diagram = state["mermaid_diagram"]
    messages = state["messages"]
    result = agent_executor.invoke({"input": mermaid_diagram,"messages": messages})
    messages.append(HumanMessage(content=result["output"]))
    return {"messages":messages,"mermaid_diagram":result["mermaid_diagram"]}

def check_mermaid_node(state: GraphState):
    """
    This is a node in the graph.
    """
    mermaid_diagram = state["mermaid_diagram"]
    result = tool_executor.invoke({"input":mermaid_diagram})
    return {"messages":state["messages"],"mermaid_diagram":result}

# --- Define the conditional edges ---

def should_continue(state):
    """
    Checks if we should continue fixing the mermaid diagram.
    """
    return "continue" if "Error:" in state["mermaid_diagram"] else "end"
# --- Build the graph ---

graph = StateGraph(GraphState)
graph.add_node("check", check_mermaid_node)
graph.add_node("fix", fix_mermaid_node)
graph.set_entry_point("check")
graph.add_conditional_edges(
    "check",
    should_continue,
    {
        "continue": "fix",
        "end": END
    }
)
graph.add_edge("fix", "check")

graph = graph.compile()

# --- Example usage ---
# test_diagram = """
# graph TD
#     A[Start] --> B{Is it?};
#     B -- Yes --> C[OK];
#     B -- No ----> D[KO];
#     C --> E[End];
#     D --> E;
# """
# graph.invoke({"mermaid_diagram":test_diagram,"messages":[]})
