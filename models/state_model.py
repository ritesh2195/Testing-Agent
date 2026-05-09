from langchain_core.messages import AnyMessage, BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from models.test_case_model import TestSuite
from typing import Annotated, List, Optional

class StateModel(BaseModel):
    """Model to represent the state of the testing agent"""
    issue_id: str = Field(description="jira ticket id")
    requirements:Optional[str] = Field(default=None,description="requirements in BDD format")
    test_cases:Optional[TestSuite] = Field(default=None,description="test cases")
    messages:Annotated[list[AnyMessage],add_messages]