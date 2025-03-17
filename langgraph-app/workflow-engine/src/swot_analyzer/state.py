"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence 

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing_extensions import Annotated


@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )

@dataclass
class State(InputState):
   motivational_quote: Optional[str] = None
   strenths: Optional[List[str]] = None
   weaknesses: Optional[List[str]] = None
   opportunities: Optional[List[str]] = None
   threats: Optional[List[str]] = None 
   analysis_summary: Optional[str] = None 