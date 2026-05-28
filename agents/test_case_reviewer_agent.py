from models.state_model import StateModel
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from prompts.test_case_review_prompt import get_test_review_prompt
from models.test_case_review_model import TestCaseReport

def review_test_case_agent(state: StateModel):

    llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.1)

    parser = PydanticOutputParser(pydantic_object=TestCaseReport)

    prompt = get_test_review_prompt().partial(format_instructions=parser.get_format_instructions())

    formatted_prompt = prompt.invoke({
        "test_cases":state.test_cases,
        "requirements":state.requirements
    })

    llm_response = llm.invoke(formatted_prompt)

    parsed_output = parser.invoke(llm_response)

    return {
        "review_comments":parsed_output
    }

    