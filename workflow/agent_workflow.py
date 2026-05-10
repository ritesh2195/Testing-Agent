from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from models.state_model import StateModel
from langgraph.prebuilt.tool_node import tools_condition
from agents.test_case_generation_agent import generate_test_case_generation_agent
from agents.test_case_reviewer_agent import review_test_case_agent
from tools.jira_tool import get_jira_ticket_details

def should_regenerate_test_cases(state: StateModel):

    if state.iteration_count >= 2:
        return END

    if len(state.review_comments.issues) > 0:
        return "agent"

    return END

def build_workflow():
    tools = [get_jira_ticket_details]

    graph = StateGraph(StateModel)

    graph.add_node("agent",generate_test_case_generation_agent)

    graph.add_node("tools",ToolNode(tools))

    graph.add_node("review_agent",review_test_case_agent)

    graph.add_edge(START, "agent")

    graph.add_conditional_edges("agent",tools_condition)

    graph.add_edge("tools", "agent")

    graph.add_edge("agent","review_agent")

    graph.add_conditional_edges(
    "review_agent",
    should_regenerate_test_cases,
    {
        "agent": "agent",
        END: END
    }
    )

    app = graph.compile()

    return app
