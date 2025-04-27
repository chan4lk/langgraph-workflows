
from dataclasses import dataclass, field
from typing import List

from langchain_core.messages import AnyMessage

@dataclass
class BookstoreState:
    """State for the bookstore workflow."""
    messages: List[AnyMessage] = field(default_factory=list)