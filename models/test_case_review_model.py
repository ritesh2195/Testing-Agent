from pydantic import BaseModel, Field
from typing import Optional, List

class ReviewIssue(BaseModel):
    category:str = Field(description="categoty of review")
    severity:str = Field(description="severity of review")
    test_case_title: str = Field(description="Related test case title")
    issue:str = Field(description="Problem identified in the test case")
    suggestion:str = Field(description="suggestion to improve test case")

class TestCaseReport(BaseModel):
    overall_comment:str = Field(description="overall comment in test suit")
    issues:List[ReviewIssue] = Field(description="list of review comments")
    recommendations: List[str] = Field(description="General recommendations for improving the suite")