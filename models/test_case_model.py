from pydantic import BaseModel, Field
from typing import List

class TestCase(BaseModel):
    """Single test case model"""
    title: str = Field(description="A title for the test case")
    steps: List[str] = Field(description="The steps to execute the test case")
    expected_result: str = Field(description="The expected result of the test case")

class TestSuite(BaseModel):
    """Container for multiple test cases"""
    test_cases: List[TestCase] = Field(
        description="List of test cases covering positive, negative, and edge scenarios"
    )