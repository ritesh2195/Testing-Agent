from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from models.test_case_model import TestSuite
from prompts.test_case_prompt import get_test_generation_prompt
from dotenv import load_dotenv
import os
from tools.jira_tool import get_jira_ticket_details

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def create_test_generation_chain(model: str = "gpt-4o-mini", temperature: float = 0.7):
    tools = [get_jira_ticket_details]

    parser = PydanticOutputParser(pydantic_object=TestSuite)

    prompt = prompt = get_test_generation_prompt().partial(
        format_instructions=parser.get_format_instructions()
    )

    llm = ChatOpenAI(model=model, temperature=temperature)

    chain = prompt | llm | parser

    return chain

    """agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor, parser"""