from chains.test_case_generation_chain import create_test_generation_c, create_test_generation_chain, create_test_generation_chainhain
from tools.jira_tool import get_jira_ticket_details


def main():
    chain = create_test_generation_chain()
    result = chain.invoke({
        "jira_ticket_id": get_jira_ticket_details("SCRUM-6")
    })

    print(f"Generated {len(result.test_cases)} test cases\n")

    for i, test_case in enumerate(result.test_cases, 1):
        print(f"Test Case {i}: {test_case.title}")
        print(f"   Steps: {', '.join(test_case.steps)}")
        print(f"   Expected: {test_case.expected_result}")
        print("-" * 50)


if __name__ == "__main__":
    main()