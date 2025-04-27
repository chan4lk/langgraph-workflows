
from langchain_core.tools import Tool
from pydantic import BaseModel, Field


class UserInput(BaseModel):
    name: str = Field(description="User's name")


def get_user_details(name: str) -> str:
    """Get user details"""
    USERS = [
        {"name": "Chandima", "role": "Software Engineer"},
        {"name": "Logan", "role": "Product Manager"},
        {"name": "Hank", "role": "Software Intern"},
    ]

    for user in USERS:
        if user["name"].lower() == name.lower():
            return user["role"]
    return "NOT_FOUND"

get_user_details_tool = Tool(
    name="get_user_details",
    description="Get user details",
    args_schema=UserInput,
    return_direct=True,
    func=get_user_details
)