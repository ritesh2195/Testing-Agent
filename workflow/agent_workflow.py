from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt.tool_node import tools_condition
from models.state_model import StateModel
from agents.test_case_generation_agent import (generate_test_case_generation_agent)
from agents.test_case_reviewer_agent import (review_test_case_agent)
from agents.test_automation_agent import (create_automation_script_agent)
from tools.jira_tool import get_jira_ticket_details


def should_regenerate_test_cases(state: StateModel):

    # Stop regeneration after 2 iterations
    if state.iteration_count >= 2:
        return "automation_agent"

    # If review issues exist → regenerate
    if len(state.review_comments.issues) > 0:
        return "agent"

    # If review passed → generate automation
    return "automation_agent"


def build_workflow():

    tools = [get_jira_ticket_details]

    graph = StateGraph(StateModel)

    # Nodes
    graph.add_node(
        "agent",
        generate_test_case_generation_agent
    )

    graph.add_node(
        "tools",
        ToolNode(tools)
    )

    graph.add_node(
        "review_agent",
        review_test_case_agent
    )

    graph.add_node(
        "automation_agent",
        create_automation_script_agent
    )

    # Start
    graph.add_edge(START, "agent")

    # Tool handling
    graph.add_conditional_edges(
        "agent",
        tools_condition
    )

    graph.add_edge("tools", "agent")

    # Review flow
    graph.add_edge("agent", "review_agent")

    # Decide regenerate or automate
    graph.add_conditional_edges(
        "review_agent",
        should_regenerate_test_cases,
        {
            "agent": "agent",
            "automation_agent": "automation_agent"
        }
    )

    # Final step
    graph.add_edge("automation_agent", END)

    return graph.compile()