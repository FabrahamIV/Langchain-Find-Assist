from app.schemas.chat_schemas import ChatState
from langgraph.graph import StateGraph, END
from typing import Literal
# Import agents_nodes here to avoid circular imports since agents_nodes imports generate_reply
from app.agents.agents_nodes import process_file_node, retrieve_node, reply_node, route_based_on_file


def build_chat_graph():
    """
    Build LangGraph workflow for RAG chat.
    """
    builder = StateGraph(ChatState)

    # Nodes
    builder.add_node("process_file", process_file_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("generate", reply_node)

    # Flow
    builder.set_conditional_entry_point(
        route_based_on_file,
        {
            "process_file_node": "process_file",
            "retrieve_node": "retrieve",
        }
    )
    builder.add_edge("process_file", "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    graph = builder.compile()

    return graph


# create graph instance
app_graph = build_chat_graph()
chat_graph = app_graph