from workflow.agent_workflow import build_workflow


def main():

    workflow = build_workflow()

    result = workflow.invoke({"issue_id":"SCRUM-6","messages": []})

    test_suite = result["test_cases"]

    print(f"Generated {len(test_suite.test_cases)} test cases\n")

    for i, test_case in enumerate(test_suite.test_cases, 1):
        print(f"Test Case {i}: {test_case.title}")
        print(f"   Steps: {', '.join(test_case.steps)}")
        print(f"   Expected: {test_case.expected_result}")
        print("-" * 50)


if __name__ == "__main__":
    main()