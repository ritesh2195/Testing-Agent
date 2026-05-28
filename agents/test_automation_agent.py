from models.state_model import StateModel
from langchain_openai import ChatOpenAI
from prompts.test_automation_prompt import get_automation_prompt

def create_automation_script_agent(state:StateModel):
    llm = ChatOpenAI(model="gpt-4.1",temperature=0.1)
    prompt = get_automation_prompt()
    chain = prompt|llm
    response = chain.invoke({
        "requirements": state.test_cases.model_dump_json(indent=2)
    })
    return {
        "automation_code": response.content
    }
