from langchain_core.prompts import ChatPromptTemplate


def get_test_generation_prompt():
    return ChatPromptTemplate.from_messages([
        ("system",
        "You are a senior QA automation engineer.\n"
        "Your task is to convert a Jira user story into STRICT structured test cases.\n\n"
        "IMPORTANT RULES:\n"
        "- DO NOT return Jira summary or description\n"
        "- DO NOT repeat input fields\n"
        "- ONLY return structured test cases in the given schema\n"
        "- Generate multiple test cases including positive, negative, and edge cases\n\n"
        "{format_instructions}"
        ),
        ("human",
        "JIRA Ticket ID: {jira_ticket_id}\n\n"
        "Convert this Jira story into structured test cases only.\n"
)
    ])