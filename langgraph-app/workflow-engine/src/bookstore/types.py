from typing import Dict, Optional, Any, List, Union, Literal
from dataclasses import dataclass, field
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage

# Define the state keys for the bookstore workflow
class BookstoreKeys(TypedDict):
    user_request: str
    book_info: Optional[Dict[str, Any]]
    catalog_update_status: Optional[Dict[str, Any]]
    next_step: str
    error: Optional[str]
    filter_tools: Optional[List[str]]

# Define the main state object for the workflow
@dataclass
class BookstoreState:
    keys: Optional[BookstoreKeys] = None
    user_request: Optional[str] = None
    messages: Optional[List[Union[Dict[str, Any], BaseMessage]]] = None
    all_messages: Optional[List[BaseMessage]] = None
    filter_tools: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.user_request is not None:
            self.keys["user_request"] = self.user_request
        
        # Initialize messages list if not provided
        if self.messages is None:
            self.messages = []
            
        # Initialize all_messages list if not provided
        if self.all_messages is None:
            self.all_messages = []

        # Init keys if not provided
        if self.keys is None:
            self.keys = {}
            
        # Initialize filter_tools if not in keys
        if "filter_tools" not in self.keys:
            self.keys["filter_tools"] = self.filter_tools

# Define the possible next steps
NextStep = Literal["book_info_provider", "catalog_updater", "FINISH"]
