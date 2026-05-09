from langchain_core.prompts import ChatPromptTemplate


def get_test_generation_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a senior QA automation engineer.\n"
            "Generate structured API test cases.\n\n"
            "{format_instructions}"
        ),

        (
            "human",
            "Jira Story:\n"
            "{requirements}\n\n"
            "Generate positive, negative, and edge test cases."
        )
    ])