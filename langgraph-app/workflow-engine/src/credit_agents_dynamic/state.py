from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Union, Any
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage, HumanMessage
# Define the state for our credit approval workflow
class ApplicationStatus(Enum):
    PENDING = auto()
    CREDIT_CHECK = auto()
    KYC_CHECK = auto()
    INCOME_VERIFICATION = auto()
    BACKGROUND_CHECK = auto()
    MANUAL_APPROVAL = auto()
    FINAL_DECISION = auto()
    APPROVED = auto()
    REJECTED = auto()

class CreditKeys(TypedDict):
    application_id: str
    customer_id: str
    product_type: str
    requested_amount: float
    credit_score: Optional[int]
    kyc_passed: Optional[bool]
    income_verified: Optional[bool]
    background_check_passed: Optional[bool]
    manual_approval_needed: Optional[bool]
    manual_approval_result: Optional[bool]
    final_decision: Optional[str]
    status: ApplicationStatus

@dataclass
class CreditState:
    keys: CreditKeys
    next: str = "supervisor"
    messages: List[Union[HumanMessage, AIMessage]] = field(default_factory=list)
