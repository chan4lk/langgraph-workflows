from langchain_openai import ChatOpenAI
from .prompts import STRENGTHS_PROMPT, WEAKNESSES_PROMPT, OPPORTUNITIES_PROMPT, THREATS_PROMPT, SUMMARY_PROMPT, GREETING_PROMPT
from typing import Dict, Any
from langchain_core.tools import tool
from langgraph.types import interrupt
from langchain_core.messages import AIMessage

# Import the SWOTState class from swot_agent
# Note: Using a string to avoid circular import
from typing import TYPE_CHECKING
from swot_analyzer.state import State, InputState

LM_STUDIO_API_URL = "http://127.0.0.1:1234/v1"  # Base URL for LM Studio API

llm = ChatOpenAI(
    base_url=LM_STUDIO_API_URL,
    temperature=0,
    max_tokens=100,
    api_key="not-needed",  # Dummy API key, not required for LM Studio in local mode
)


def call_lm_studio(prompt: str) -> str:
    """
    Calls LM Studio API using Langchain ChatOpenAI.
    """
    try:
        print(f"\nAttempting to call LM Studio at {LM_STUDIO_API_URL}")
        print(f"Prompt being sent: {prompt}")
        response = llm.predict(prompt)
        print(f"Response received: {response}")
        return response
    except Exception as e:
        print(f"\nError calling LM Studio: {str(e)}")
        print(f"Full error details: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return "Error communicating with LM Studio."


def get_human_input(component: str) -> str:
    """
    Get human input for a specific SWOT component.
    """
    human_response = interrupt({"query": f"Please provide information about {component} for the SWOT analysis:"})
    return human_response["data"]


def strengths_node(state: InputState):
    """
    Node to identify strengths using LM Studio.
    """
    print("Strengths Node")
    # Get human input first
    human_input = get_human_input("strengths")
    prompt = STRENGTHS_PROMPT.format(user_input=human_input)
    strengths = call_lm_studio(prompt)
    state.strenths = strengths
    return state


def weaknesses_node(state: State):
    """
    Node to identify weaknesses using LM Studio.
    """
    print("Weaknesses Node")
    # Get human input first
    human_input = get_human_input("weaknesses")
    prompt = WEAKNESSES_PROMPT.format(user_input=human_input)
    weaknesses = call_lm_studio(prompt)
    state.weaknesses = weaknesses
    return state


def opportunities_node(state: State):
    """
    Node to identify opportunities using LM Studio.
    """
    print("Opportunities Node")
    # Get human input first
    human_input = get_human_input("opportunities")
    prompt = OPPORTUNITIES_PROMPT.format(user_input=human_input)
    opportunities = call_lm_studio(prompt)
    state.opportunities = opportunities
    return state


def threats_node(state: State):
    """
    Node to identify threats using LM Studio.
    """
    print("Threats Node")
    # Get human input first
    human_input = get_human_input("threats")
    prompt = THREATS_PROMPT.format(user_input=human_input)
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


def greetings_node(state: InputState):
    """
    Node to generate a motivational quote using LM Studio and add it to messages.
    """
    print("Greetings Node")
    prompt = GREETING_PROMPT
    motivational_quote = call_lm_studio(prompt)
    
    # Store the quote in the state
    state.motivational_quote = motivational_quote
    
    # Add the motivational quote to the messages array
    quote_message = AIMessage(content=f"Welcome to SWOT Analysis! Here's a motivational quote to inspire your strategic thinking:\n\n{motivational_quote}")
    state.messages.append(quote_message)
    
    print(f"Motivational Quote: {motivational_quote}")
    return state


def output_node(state: State):
    """
    Node to output the SWOT analysis.
    """
    print("Output Node")
    print(state.analysis_summary)
    return state
