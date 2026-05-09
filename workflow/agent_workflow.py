from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from models.state_model import StateModel
from langgraph.prebuilt.tool_node import tools_condition
from agents.test_case_generation_agent import generate_test_case_generation_agent
from tools.jira_tool import get_jira_ticket_details


def build_workflow():
    tools = [get_jira_ticket_details]

    graph = StateGraph(StateModel)
    
    graph.add_node("agent",generate_test_case_generation_agent)

    graph.add_node("tools",ToolNode(tools))

    graph.add_edge(START, "agent")

    graph.add_conditional_edges("agent",tools_condition)

    graph.add_edge("tools", "agent")

    app = graph.compile()

    return app
