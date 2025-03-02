from langchain_openai import ChatOpenAI
from .prompts import STRENGTHS_PROMPT, WEAKNESSES_PROMPT, OPPORTUNITIES_PROMPT, THREATS_PROMPT
from typing import Dict, Any

# Import the SWOTState class from swot_agent
# Note: Using a string to avoid circular import
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from swot_analyzer.swot_agent import SWOTState

LM_STUDIO_API_URL = "http://localhost:1234/v1"  # Base URL for LM Studio API

llm = ChatOpenAI(
    base_url=LM_STUDIO_API_URL,
    temperature=0,
    api_key="not-needed",  # Dummy API key, not required for LM Studio in local mode
)


def call_lm_studio(prompt: str) -> str:
    """
    Calls LM Studio API using Langchain ChatOpenAI.
    """
    try:
        response = llm.predict(prompt)
        return response
    except Exception as e:
        print(f"Error calling LM Studio: {e}")
        return "Error communicating with LM Studio."


def strengths_node(state):
    """
    Node to identify strengths using LM Studio.
    """
    print("Strengths Node")
    prompt = STRENGTHS_PROMPT.format(user_input=state.keys.get("user_input", ""))
    strengths = call_lm_studio(prompt)
    state.keys["strengths"] = strengths
    return state


def weaknesses_node(state):
    """
    Node to identify weaknesses using LM Studio.
    """
    print("Weaknesses Node")
    prompt = WEAKNESSES_PROMPT.format(user_input=state.keys.get("user_input", ""))
    weaknesses = call_lm_studio(prompt)
    state.keys["weaknesses"] = weaknesses
    return state


def opportunities_node(state):
    """
    Node to identify opportunities using LM Studio.
    """
    print("Opportunities Node")
    prompt = OPPORTUNITIES_PROMPT.format(user_input=state.keys.get("user_input", ""))
    opportunities = call_lm_studio(prompt)
    state.keys["opportunities"] = opportunities
    return state


def threats_node(state):
    """
    Node to identify threats using LM Studio.
    """
    print("Threats Node")
    prompt = THREATS_PROMPT.format(user_input=state.keys.get("user_input", ""))
    threats = call_lm_studio(prompt)
    state.keys["threats"] = threats
    return state


def summarize_analysis(state):
    """
    Node to summarize the SWOT analysis.
    """
    print("Summarize Analysis Node")
    strengths = state.keys.get("strengths", "Not found")
    weaknesses = state.keys.get("weaknesses", "Not found")
    opportunities = state.keys.get("opportunities", "Not found")
    threats = state.keys.get("threats", "Not found")

    analysis_summary = f"""
    SWOT Analysis Summary:

    Strengths: {strengths}
    Weaknesses: {weaknesses}
    Opportunities: {opportunities}
    Threats: {threats}
    """
    state.keys["analysis_summary"] = analysis_summary
    return state


def output_node(state):
    """
    Node to output the SWOT analysis.
    """
    print("Output Node")
    print(state.keys.get("analysis_summary", "No analysis summary available"))
    return state
