from langgraph.graph import StateGraph, END
from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from dataclasses import dataclass, field
from langgraph.types import interrupt  # Import the simpler interrupt function
from swot_analyzer.nodes import strengths_node, weaknesses_node, opportunities_node, threats_node, summarize_analysis, output_node

class SWOTKeys(TypedDict, total=False):
    user_input: str
    strengths: str
    weaknesses: str
    opportunities: str
    threats: str
    analysis_summary: str

@dataclass
class SWOTState:
    """State for the SWOT analysis agent."""
    keys: SWOTKeys = field(default_factory=dict)
    user_input: Optional[str] = None
    
    def __post_init__(self):
        if self.user_input and "user_input" not in self.keys:
            self.keys["user_input"] = self.user_input


def start_node(state: SWOTState):
    """Start node; handles user input using simpler interrupt."""
    if not state.keys.get("user_input"):
        user_input = interrupt("user_input_prompt")
        if user_input:  # Check if the interrupt was resolved (input received)
            state.keys["user_input"] = user_input
        else:
            return None  # If it is None it will go to start again.

    # We don't need to return a new state with keys, just return the state itself
    return state


# Build the LangGraph state graph
workflow = StateGraph(SWOTState)

# ... (rest of your node definitions remain the same) ...
workflow.add_node("start", start_node)
workflow.add_node("strengths", strengths_node)
workflow.add_node("weaknesses", weaknesses_node)
workflow.add_node("opportunities", opportunities_node)
workflow.add_node("threats", threats_node)
workflow.add_node("summarize", summarize_analysis)
workflow.add_node("output", output_node)


# Define edges (simpler, no conditional edges needed)
workflow.set_entry_point("start")
workflow.add_edge("start", "strengths")
workflow.add_edge("strengths", "weaknesses")
workflow.add_edge("weaknesses", "opportunities")
workflow.add_edge("opportunities", "threats")
workflow.add_edge("threats", "summarize")
workflow.add_edge("summarize", "output")
workflow.add_edge("output", END)

# Compile the graph
graph = workflow.compile()
