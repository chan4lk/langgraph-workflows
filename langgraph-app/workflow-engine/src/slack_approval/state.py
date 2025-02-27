"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Any

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from typing_extensions import Annotated


@dataclass
class InputState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    slack_event: Optional[Dict[str, Any]] = None


@dataclass
class LeadAttributes:
    geo_location: Optional[str] = None
    industry: Optional[str] = None
    engagement: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "geo_location": self.geo_location,
            "industry": self.industry,
            "engagement": self.engagement
        }


@dataclass
class State(InputState):
    is_last_step: IsLastStep = field(default=False)
    lead_attributes: Optional[LeadAttributes] = None
    assigned_sales_person: Optional[str] = None
    approval_status: Optional[bool] = None
    hubspot_lead_created: bool = False
    notification_sent: bool = False