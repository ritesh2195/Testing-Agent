from workflow.agent_workflow import build_workflow

def main():

    workflow = build_workflow()

    result = workflow.invoke({"issue_id":"SCRUM-6","messages": []})

    print(result["automation_code"])


if __name__ == "__main__":
    main()