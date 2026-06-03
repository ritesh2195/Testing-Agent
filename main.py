from workflow.agent_workflow import build_workflow
from utils.file_util import save_to_file
from utils.excel_file_util import ExcelUtil

def main():

    workflow = build_workflow()

    result = workflow.invoke({"issue_id":"SCRUM-6","messages": []})

    excel_util = ExcelUtil("file/test_cases.xlsx")

    excel_util = ExcelUtil("docs/test_cases.xlsx")

    excel_util.export(result['test_cases'])

    save_to_file(result["automation_code"],"client/api.ts")


if __name__ == "__main__":
    main()