from langchain.tools import tool
import requests

from config import JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_EMAIL

@tool("get_jira_ticket_details", return_direct=True)
def get_jira_ticket_details(ticket_id: str) -> str:
    """
    Fetch Jira ticket details using the Jira REST API.

    This tool retrieves the summary and description of a Jira issue
    based on the provided ticket ID.

    Args:
        ticket_id (str): Jira issue key

    Returns:
        str: Formatted Jira ticket details containing:
            - Summary
            - Description
    """
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{ticket_id}"
    r = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), timeout=30)
    r.raise_for_status()
    data = r.json()
    return f"""
    Summary: {data["fields"]["summary"]}
    Description: {data["fields"].get("description", "")}
    """