from langchain_openai import ChatOpenAI
from .prompts import STRENGTHS_PROMPT, WEAKNESSES_PROMPT, OPPORTUNITIES_PROMPT, THREATS_PROMPT, SUMMARY_PROMPT 
from typing import Dict, Any

# Import the SWOTState class from swot_agent
# Note: Using a string to avoid circular import
from typing import TYPE_CHECKING
from swot_analyzer.state import State

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


def strengths_node(state: State):
    """
    Node to identify strengths using LM Studio.
    """
    print("Strengths Node")
    prompt = STRENGTHS_PROMPT.format(user_input=state.messages[-1].content)
    strengths = call_lm_studio(prompt)
    state.strenths = strengths
    return state


def weaknesses_node(state: State):
    """
    Node to identify weaknesses using LM Studio.
    """
    print("Weaknesses Node")
    prompt = WEAKNESSES_PROMPT.format(user_input=state.messages[-1].content)
    weaknesses = call_lm_studio(prompt)
    state.weaknesses = weaknesses
    return state


def opportunities_node(state: State):
    """
    Node to identify opportunities using LM Studio.
    """
    print("Opportunities Node")
    prompt = OPPORTUNITIES_PROMPT.format(user_input=state.messages[-1].content)
    opportunities = call_lm_studio(prompt)
    state.opportunities = opportunities
    return state


def threats_node(state: State):
    """
    Node to identify threats using LM Studio.
    """
    print("Threats Node")
    prompt = THREATS_PROMPT.format(user_input=state.messages[-1].content)
    threats = call_lm_studio(prompt)
    state.threats = threats
    return state


def summarize_analysis(state: State):
    """
    Node to summarize the SWOT analysis.
    """
    print("Summarize Analysis Node")
    prompt = SUMMARY_PROMPT.format(
        strengths=state.strenths,
        weaknesses=state.weaknesses,
        opportunities=state.opportunities,
        threats=state.threats,
    )
    analysis_summary = call_lm_studio(prompt)
    state.analysis_summary = analysis_summary
    return state


def output_node(state: State):
    """
    Node to output the SWOT analysis.
    """
    print("Output Node")
    print(state.analysis_summary)
    return state
