from langchain_core.messages import AnyMessage, BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field
from models.test_case_model import TestSuite
from typing import Annotated, List, Optional
from models.test_case_review_model import TestCaseReport

class StateModel(BaseModel):
    """Model to represent the state of the testing agent"""
    messages:Annotated[list[AnyMessage],add_messages]
    issue_id: str = Field(description="jira ticket id")
    requirements:Optional[str] = Field(default=None,description="requirements in BDD format")
    test_cases:Optional[TestSuite] = Field(default=None,description="test cases")
    review_comments:Optional[TestCaseReport] = Field(default=None, description="review comment provided by reviewer agent")
    iteration_count:Optional[int] = 0