from dataclasses import dataclass, field
from typing import List, Union
from langchain_core.messages import AIMessage, HumanMessage
from credit_agents_deterministic.messages import FilterableHumanMessage, FilterableAIMessage
# Define the state for our credit approval workflow
@dataclass
class CreditState:
    next: str = "supervisor"
    filter_tools: List[str] = field(default_factory=lambda: ["credit_score_checker", "background_checker"])
    messages: List[Union[HumanMessage, AIMessage]] = field(default_factory=list)
    all_messages: List[Union[FilterableHumanMessage, FilterableAIMessage]] = field(default_factory=list)
