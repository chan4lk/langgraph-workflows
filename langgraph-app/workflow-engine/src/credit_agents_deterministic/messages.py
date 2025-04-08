from langchain_core.messages import AIMessage, HumanMessage
from typing import List, Union

class FilterableAIMessage(AIMessage):
    def __init__(self, content: str, name:str, show_in_chat: bool):
        super().__init__(content, name=name)
        self.show_in_chat = show_in_chat
    
    # factory to create an instance of this class from AIMessage
    @classmethod
    def from_aimessage(cls, aimessage: AIMessage, show_in_chat: bool) -> "FilterableAIMessage":
        return cls(aimessage.content, name=aimessage.name, show_in_chat=show_in_chat)
    
    def to_aimessage(self) -> AIMessage:
        return AIMessage(content=self.content, name=self.name)

class FilterableHumanMessage(HumanMessage):
    def __init__(self, content: str, name:str, show_in_chat: bool):
        super().__init__(content, name=name)
        self.show_in_chat = show_in_chat

    # factory to create an instance of this class from HumanMessage
    @classmethod
    def from_humanmessage(cls, humanmessage: HumanMessage, show_in_chat: bool) -> "FilterableHumanMessage":
        return cls(humanmessage.content, name=humanmessage.name, show_in_chat=show_in_chat)
    
    def to_humanmessage(self) -> HumanMessage:
        return HumanMessage(content=self.content, name=self.name)
    

# factory to create an instance of this class from list of messages
def create_messages(messages: List[Union[HumanMessage, AIMessage, dict]], show_in_chat: bool) -> List[Union[FilterableHumanMessage, FilterableAIMessage]]:
    print(f"create_messages - input type: {type(messages)}")
    result = []
    
    for msg in messages:
        if isinstance(msg, HumanMessage):
            result.append(FilterableHumanMessage.from_humanmessage(msg, show_in_chat))
        elif isinstance(msg, AIMessage):
            result.append(FilterableAIMessage.from_aimessage(msg, show_in_chat))
        elif isinstance(msg, dict) and 'content' in msg:
            # Handle dictionary messages
            msg_type = msg.get('type', 'human')  # Default to human if type not specified
            msg_content = msg['content']
            msg_name = msg.get('name', None)
            
            if msg_type == 'human':
                human_msg = HumanMessage(content=msg_content, name=msg_name)
                result.append(FilterableHumanMessage.from_humanmessage(human_msg, show_in_chat))
            elif msg_type == 'ai':
                ai_msg = AIMessage(content=msg_content, name=msg_name)
                result.append(FilterableAIMessage.from_aimessage(ai_msg, show_in_chat))
        else:
            print(f"Unknown message type: {type(msg)}, content: {msg}")
    
    print(f"create_messages - created {len(result)} filterable messages")
    return result

# factory to create an instance of HumanMessage or AIMessage from list of FilterableHumanMessage or FilterableAIMessage
def reverse_messages(messages: List[Union[FilterableHumanMessage, FilterableAIMessage]]) -> List[Union[HumanMessage, AIMessage]]:
    print(f"reverse_messages - input type: {type(messages)}")
    
    if not messages:
        print("Warning: Empty messages list passed to reverse_messages")
        return []
    
    result = []
    for msg in messages:
        if isinstance(msg, FilterableHumanMessage):
            result.append(msg.to_humanmessage())
        elif isinstance(msg, FilterableAIMessage):
            result.append(msg.to_aimessage())
        elif isinstance(msg, HumanMessage):
            # Already a HumanMessage, just add it
            result.append(msg)
        elif isinstance(msg, AIMessage):
            # Already an AIMessage, just add it
            result.append(msg)
        elif isinstance(msg, dict) and 'content' in msg:
            # Handle dictionary messages
            msg_type = msg.get('type', 'human')  # Default to human if type not specified
            msg_content = msg['content']
            msg_name = msg.get('name', None)
            
            if msg_type == 'human':
                result.append(HumanMessage(content=msg_content, name=msg_name))
            elif msg_type == 'ai':
                result.append(AIMessage(content=msg_content, name=msg_name))
        else:
            print(f"Unknown message type: {type(msg)}, content: {msg}")
    
    print(f"reverse_messages - converted {len(result)} messages")
    return result

def filter_messages(messages: List[Union[FilterableHumanMessage, FilterableAIMessage]], show_in_chat: bool) -> List[Union[FilterableHumanMessage, FilterableAIMessage]]:
    return [msg for msg in messages if not hasattr(msg, 'show_in_chat') or msg.show_in_chat == show_in_chat]


def normalize_messages(messages: List[Union[dict, HumanMessage, AIMessage]]) -> List[Union[HumanMessage, AIMessage]]:
    """
    Normalize messages to ensure they are proper HumanMessage or AIMessage objects.
    This handles conversion from dictionaries or other formats to the proper message types.
    
    Args:
        messages: A list of messages in various formats (dict, HumanMessage, AIMessage)
        
    Returns:
        A list of properly formatted HumanMessage and AIMessage objects
    """
    if not messages:
        return []
        
    result = []
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage)):
            # Already a proper message object
            result.append(msg)
        elif isinstance(msg, dict) and 'content' in msg:
            # Convert dictionary to proper message object
            msg_type = msg.get('type', 'human')  # Default to human if type not specified
            msg_content = msg['content']
            msg_name = msg.get('name', None)
            
            if msg_type == 'human':
                result.append(HumanMessage(content=msg_content, name=msg_name))
            elif msg_type == 'ai':
                result.append(AIMessage(content=msg_content, name=msg_name))
        else:
            print(f"Warning: Unknown message format: {type(msg)}, content: {msg}")
    
    return result