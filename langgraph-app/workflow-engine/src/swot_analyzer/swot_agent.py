from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from langgraph.types import interrupt
from swot_analyzer.state import State
from swot_analyzer.nodes import greetings_node, strengths_node, weaknesses_node, opportunities_node, threats_node, output_node, summarize_analysis

graph_builder = StateGraph ( State )

@tool
def human_assistance ( query : str ) -> str :
    """Request assistance from a human."""
    human_response = interrupt ({ "query" : query })
    return human_response [ "data" ]

graph_builder.add_node("greetings_node", greetings_node)
graph_builder.add_node("strengths_node", strengths_node)
graph_builder.add_node("weaknesses_node", weaknesses_node)
graph_builder.add_node("opportunities_node", opportunities_node)
graph_builder.add_node("threats_node", threats_node)
graph_builder.add_node("summarize_analysis_node", summarize_analysis)
graph_builder.add_node("output_node", output_node)

graph_builder.add_edge( START , "greetings_node" )
graph_builder.add_edge( "greetings_node" , "strengths_node" )
graph_builder.add_edge( "strengths_node" , "weaknesses_node" )
graph_builder.add_edge( "weaknesses_node" , "opportunities_node" )
graph_builder.add_edge( "opportunities_node" , "threats_node" )
graph_builder.add_edge( "threats_node" , "summarize_analysis_node" )
graph_builder.add_edge( "summarize_analysis_node" , "output_node" )
graph_builder.add_edge( "output_node" ,  END )

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)