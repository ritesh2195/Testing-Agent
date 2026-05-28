from langchain_core.prompts import ChatPromptTemplate


def get_automation_prompt():
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a senior QA automation engineer.

Generate clean, production-ready Playwright TypeScript automation code.

Rules:
- Use standalone Playwright code
- Do not assume any existing framework
- Keep everything in one file
- Use Playwright test runner
- Use async/await properly
- Generate a separate test() method for EACH test case
- Each test case should be independent
- Use meaningful test names based on test case titles
- Add meaningful assertions
- Cover positive, negative, and edge scenarios
- Avoid unnecessary abstractions
- Reuse helper functions only if truly needed
- Use proper APIRequestContext creation if API testing
- Use proper browser/page setup if UI testing
- Return only executable TypeScript code

Code Structure Requirements:
- Import required Playwright modules
- Add test.describe block
- Create separate test methods for every test case
- Keep setup reusable
- Keep assertions clear and readable
"""
            ),
            (
                "human",
                """
Generate Playwright TypeScript automation code for the following test cases.

Test Cases:
{requirements}
"""
            )
        ]
    )