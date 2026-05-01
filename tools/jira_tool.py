from langchain.tools import tool
import requests

from config import JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_EMAIL

#@tool("get_jira_ticket_details", return_direct=True)
def get_jira_ticket_details(ticket_id: str) -> str:
    """
    Simulate fetching details for a Jira ticket.
    In a real implementation, this would call the Jira API.
    """
    url = f"{JIRA_BASE_URL}/rest/api/2/issue/{ticket_id}"
    r = requests.get(url, auth=(JIRA_EMAIL, JIRA_API_TOKEN), timeout=30)
    r.raise_for_status()
    data = r.json()
    return {
        "summary": data["fields"]["summary"],
        "description": data["fields"].get("description", "")
    }