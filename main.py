from workflow.agent_workflow import build_workflow


def main():

    workflow = build_workflow()

    result = workflow.invoke({"issue_id":"SCRUM-6","messages": []})

    # for i, review in enumerate(result["review_comments"].issues, 1):
    #     print(f"\nReview {i}")
    #     print(f"Category       : {review.category}")
    #     print(f"Severity       : {review.severity}")
    #     print(f"Test Case      : {review.test_case_title}")
    #     print(f"Issue          : {review.issue}")
    #     print(f"Suggestion     : {review.suggestion}")
    #     print("-" * 60)

    test_suite = result["test_cases"]

    print(f"Generated {len(test_suite.test_cases)} test cases\n")

    for i, test_case in enumerate(test_suite.test_cases, 1):
        print(f"Test Case {i}: {test_case.title}")
        print(f"   Steps: {', '.join(test_case.steps)}")
        print(f"   Expected: {test_case.expected_result}")
        print("-" * 50)


if __name__ == "__main__":
    main()