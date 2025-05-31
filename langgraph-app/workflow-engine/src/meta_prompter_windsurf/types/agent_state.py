"""
Agent state definition for the meta prompter Windsurf workflow.
"""
from typing import Dict, List, Sequence, Optional
from typing_extensions import Annotated
from dataclasses import field, dataclass
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


@dataclass
class AgentState:
    """State for the meta prompter agent."""
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(default_factory=list)
    app_requirements: Dict = field(default_factory=dict)
    ui_flows: List[Dict] = field(default_factory=list)
    ui_prompts: List[str] = field(default_factory=list)
    architecture_prompts: List[Dict] = field(default_factory=list)
    tech_stack_choice: Optional[str] = field(default=None)
    app_building_prompts: List[Dict] = field(default_factory=list)
    ui_automation_prompts: List[Dict] = field(default_factory=list)
    current_step: str = field(default="analyze_requirements")
    
    def __repr__(self) -> str:
        """String representation of the state."""
        return f"AgentState(current_step={self.current_step})"
