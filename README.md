# AI Test Automation Agent

An AI-powered QA automation workflow built using LangGraph, LangChain, and OpenAI.

The system automatically:

1. Retrieves requirements from Jira
2. Generates API test cases
3. Reviews generated test cases for quality and coverage
4. Regenerates test cases when issues are found
5. Generates Playwright automation code from approved test cases

---

## Features

### Jira Integration

* Fetches Jira story details using Jira REST API
* Extracts summary and description
* Uses Jira requirements as input for test generation

### Test Case Generation Agent

Generates:

* Positive test cases
* Negative test cases
* Boundary value test cases
* Edge cases
* Validation scenarios
* Error handling scenarios

Output is structured using Pydantic models.

### Test Case Review Agent

Reviews generated test cases against QA best practices.

Checks for:

* Missing validation scenarios
* Missing negative scenarios
* Missing edge cases
* Missing security tests
* Weak assertions
* Incomplete expected results
* Duplicate coverage

Produces structured review comments.

### Regeneration Loop

The workflow supports iterative improvement.

Flow:

Generate Test Cases
→ Review Test Cases
→ If issues found → Regenerate
→ Review Again
→ Continue until approved or max iterations reached

### Automation Code Generation Agent

Generates:

* Playwright TypeScript API tests
* Separate test method for each test case
* Production-ready automation code
* Meaningful assertions
* Reusable setup and API context

---

## Architecture

```text
START
  |
  v
Test Case Generator
  |
  v
Test Case Reviewer
  |
  +----------------------+
  | Issues Found         |
  |                      |
  v                      |
Regenerate Test Cases    |
  |                      |
  +----------------------+
  |
  v
Automation Generator
  |
  v
END
```

---

## Tech Stack

* Python
* LangGraph
* LangChain
* OpenAI
* Pydantic
* Jira REST API
* Playwright TypeScript

---

## Project Structure

```text
project/
│
├── agents/
│   ├── test_case_generation_agent.py
│   ├── test_case_reviewer_agent.py
│   └── test_automation_agent.py
│
├── prompts/
│   ├── test_case_prompt.py
│   ├── test_review_prompt.py
│   └── test_automation_prompt.py
│
├── tools/
│   └── jira_tool.py
│
├── models/
│   ├── state_model.py
│   ├── test_case_model.py
│   └── review_model.py
│
├── workflow/
│   └── workflow.py
│
├── config.py
├── main.py
└── README.md
```

---

## State Model

The workflow shares information through a central state.

```python
class StateModel(BaseModel):
    issue_id: str
    requirements: str | None
    test_cases: TestSuite | None
    review_comments: TestCaseReviewReport | None
    automation_code: str | None
    iteration_count: int = 0
```

---

## Example Usage

```python
workflow = build_workflow()

result = workflow.invoke({
    "issue_id": "SCRUM-6",
    "messages": []
})
```

Generated outputs:

* Jira requirements
* Test cases
* Review comments
* Playwright automation code

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key

JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your_email
JIRA_API_TOKEN=your_jira_token
```

---

## Goals

Reduce manual QA effort by automating the journey from requirement to automation code using AI agents and workflow orchestration.

This project demonstrates how LangGraph can be used to build multi-agent QA automation systems with review and feedback loops.
