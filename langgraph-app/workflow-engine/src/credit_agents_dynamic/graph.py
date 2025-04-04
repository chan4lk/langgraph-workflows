from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import MessagesState, END
from langgraph.types import Command
from credit_agents_dynamic.utils import load_chat_model
from credit_agents_dynamic.tools import check_credit_score, perform_background_check, verify_income, validate_kyc, make_final_decision
from credit_agents_dynamic.state import CreditState
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent

members = ["credit_score_checker", "background_checker", "final_decision"]
# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
options = members + ["FINISH"]

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {members}. "
    "Given the following user request, "
    "respond with the worker to act next. Each worker will perform a "
    "task and respond with their results and status. When finished, "
    "respond with FINISH. If credit score is unknown next worker is credit_score_checker. "
    "If the credit score is more than 700 next worker is final_decision. "
    "If the final_decision is Approved next worker is FINISH. "
    "Otherwise route to background_checker."
)


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]


llm = load_chat_model("openai/gpt-4o-mini")

def supervisor_node(state: CreditState) -> Command[Literal[*members, "__end__"]]:
    # Create base messages with system prompt
    base_messages = [
        {"role": "system", "content": system_prompt},
    ]

    messages = base_messages + state.messages
    
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})



background_checker_agent = create_react_agent(
    llm, 
    tools=[perform_background_check], 
    prompt="You are a background checker. You need to perform a background check for a CUSTOMER_ID (not application_id). Use the perform_background_check tool with the customer_id."
)


def background_checker_node(state: CreditState) -> Command[Literal["supervisor"]]:
    result = background_checker_agent.invoke({"messages": state.messages})
    
    return Command(
        update={
            "messages": state.messages + [
                HumanMessage(content=result["messages"][-1].content, name="background_checker")
            ]
        },
        goto="supervisor",
    )


# NOTE: THIS PERFORMS ARBITRARY CODE EXECUTION, WHICH CAN BE UNSAFE WHEN NOT SANDBOXED
credit_scrore_agent = create_react_agent(llm, 
 prompt="You are a credit score checker. You need to check the credit score for a CUSTOMER_ID (not application_id). Use the check_credit_score tool with the customer_id.",
 tools=[check_credit_score])


def credit_score_node(state: CreditState) -> Command[Literal["supervisor"]]:
   
    result = credit_scrore_agent.invoke({"messages": state.messages})
    
    return Command(
        update={
            "messages": state.messages + [
                HumanMessage(content=result["messages"][-1].content, name="credit_score_checker")
            ]
        },
        goto="supervisor",
    )

final_decision_agent = create_react_agent(llm,
 prompt="You are the decision maker. You must make a final decision with a reason such as 'Approved' or 'Rejected'. IMPORTANT: You must use the APPLICATION_ID (not customer_id) when calling the make_final_decision tool. The application_id will be provided in the message.",
 tools=[make_final_decision])


def final_decision_node(state: CreditState) -> Command[Literal["supervisor"]]:
    result = final_decision_agent.invoke({"messages": state.messages})
    
    return Command(
        update={
            "messages": state.messages + [
                HumanMessage(content=result["messages"][-1].content, name="final_decision")
            ]
        },
        goto="supervisor",
    )


builder = StateGraph(CreditState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("background_checker", background_checker_node)
builder.add_node("final_decision", final_decision_node)
builder.add_node("credit_score_checker", credit_score_node)
graph = builder.compile()