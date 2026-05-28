from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from models.test_case_model import TestSuite
from prompts.test_case_prompt import get_test_generation_prompt

def generate_test_case_generation_agent(state):

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    parser = PydanticOutputParser(pydantic_object=TestSuite)

    prompt = get_test_generation_prompt().partial(
        format_instructions=parser.get_format_instructions()
    )

    if state.review_comments:
        review_comments = state.review_comments.model_dump_json(indent=2)        

    formatted_prompt = prompt.invoke({
        "requirements": state.requirements,
        "review_comments":state.review_comments
    })

    llm_response = llm.invoke(formatted_prompt)

    parsed_output = parser.invoke(llm_response)

    return {
        "test_cases": parsed_output,
        "messages": [llm_response],
        "iteration_count": state.iteration_count + 1
    }