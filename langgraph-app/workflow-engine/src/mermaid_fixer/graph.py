from langgraph.graph import StateGraph, END, add_messages
from langgraph.prebuilt import ToolNode , create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage
from typing import Annotated, TypedDict, List, Dict, Sequence
from dataclasses import dataclass, field

# --- Define the state of the graph ---
@dataclass
class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    mermaid_diagram: Annotated[str, "The mermaid diagram."]
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)

# --- Create the tool for checking mermaid diagram syntax ---
@tool
def check_mermaid_syntax(diagram: str) -> str:
    """
    Checks the syntax of a Mermaid diagram using basic validation rules.
    """
    # Basic validation for common Mermaid syntax issues
    if not diagram or diagram.strip() == "":
        return "Error: The Mermaid diagram is empty."
    
    # Check for basic diagram types
    valid_starts = [
        "graph", "flowchart", "sequenceDiagram", "classDiagram", 
        "stateDiagram", "erDiagram", "gantt", "pie", "timeline"
    ]
    
    # Remove leading/trailing whitespace and check if it starts with a valid diagram type
    cleaned_diagram = diagram.strip()
    
    # Check if the diagram starts with any of the valid diagram types
    is_valid_start = any(cleaned_diagram.startswith(start) for start in valid_starts)
    if not is_valid_start:
        return "Error: The Mermaid diagram does not start with a valid diagram type (e.g., graph, flowchart, sequenceDiagram)."
    
    # Check for basic syntax errors
    if "-->" in cleaned_diagram and cleaned_diagram.startswith("graph"):
        return "Error: The Mermaid syntax is invalid. In graph diagrams, use '->' instead of '-->'."
    
    if "->" in cleaned_diagram and cleaned_diagram.startswith("sequenceDiagram"):
        return "Error: The Mermaid syntax is invalid. In sequence diagrams, use '-->>' instead of '->'."
    
    # Check for unbalanced brackets
    if cleaned_diagram.count("[") != cleaned_diagram.count("]"): 
        return "Error: The Mermaid syntax is invalid. Unbalanced square brackets."
    
    if cleaned_diagram.count("(") != cleaned_diagram.count(")"): 
        return "Error: The Mermaid syntax is invalid. Unbalanced parentheses."
    
    if cleaned_diagram.count("{") != cleaned_diagram.count("}"): 
        return "Error: The Mermaid syntax is invalid. Unbalanced curly braces."
    
    # If no basic errors found, consider it valid
    # Note: This is a simplified check and won't catch all syntax errors
    return "The Mermaid syntax is valid."

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
    llm = ChatOpenAI(model="gpt-4o-mini")
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
llm = ChatOpenAI(model="gpt-4o-mini")
agent = agent_prompt | llm

agent_executor = create_react_agent(llm, tools=tools)

# --- Define the node ---
def fix_mermaid_node(state: GraphState):
    """
    This is a node in the graph.
    """
    mermaid_diagram = state["mermaid_diagram"]
    messages = state["messages"]
    result = agent_executor.invoke({"input": mermaid_diagram, "messages": messages})
    
    # Debug the structure of the result
    print(f"Result keys: {result.keys()}")
    
    # Handle different possible response structures
    if "output" in result:
        output_content = result["output"]
        fixed_diagram = result.get("mermaid_diagram", mermaid_diagram)  # Default to original if not present
    else:
        # For newer versions of LangGraph or different models
        # The response might be in a different format
        if isinstance(result, dict) and "messages" in result:
            # Extract the last message content as the output
            last_message = result["messages"][-1] if result["messages"] else None
            output_content = last_message.content if last_message else "No output generated"
        else:
            # Fallback to string representation
            output_content = str(result)
        
        # Try to extract mermaid diagram from the result
        fixed_diagram = mermaid_diagram  # Default to original
        # Look for mermaid diagram in the output content
        if "```mermaid" in output_content:
            # Extract the mermaid diagram from markdown code block
            import re
            mermaid_match = re.search(r'```mermaid\n(.+?)\n```', output_content, re.DOTALL)
            if mermaid_match:
                fixed_diagram = mermaid_match.group(1)
    
    # Add the output as a human message
    messages.append(HumanMessage(content=output_content))
    
    return {"messages": messages, "mermaid_diagram": fixed_diagram}

def check_mermaid_node(state: GraphState):
    """
    This is a node in the graph.
    """
    mermaid_diagram = state["mermaid_diagram"]
    
    # Directly invoke the check_mermaid_syntax tool with the diagram
    result = check_mermaid_syntax.invoke(mermaid_diagram)
    
    return {"messages": state["messages"], "mermaid_diagram": result}

# --- Define the conditional edges ---

def should_continue(state):
    """
    Checks if we should continue fixing the mermaid diagram.
    """
    # Check if the mermaid_diagram contains an error message
    # The result from check_mermaid_syntax is now directly in mermaid_diagram
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
