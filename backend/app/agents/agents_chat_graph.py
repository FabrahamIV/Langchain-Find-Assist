from dotenv import load_dotenv
from app.agents.agents_state import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in insurance. You are given a question and a context. Answer the question based on the context. If the answer is not in the context, say that you cannot answer the question. Do not answer any other question. Do not make up any information. write a short structured report (a few paragraphs) on the topic. Use only the information provided."),
    ("user", "question: {question}"),
])


def generate_reply(state: ChatState) -> dict:

    question = state.get("message", "no message found")
    print(f"--- Processing Query: {question} ---")
    
    # Defensively extract string content
    raw_docs = state.get("retrieved_docs", [])
    docs_strings = []
    for doc in raw_docs:
        if hasattr(doc, "page_content"):
            docs_strings.append(doc.page_content)
        else:
            docs_strings.append(str(doc))
            
    context = "\n\n".join(docs_strings)
    if not question:
        return {"answer": "no answer found"}

    _agent_debug_log(
        hypothesis_id="H4",
        location="agents_chat_graph.generate_reply",
        message="Starting generate reply",
        data={"query": question, "context": context},
    )

    chain = SYSTEM_PROMPT | llm
    response = chain.invoke({"question": question, "context": context})

    return {"answer": response.content}

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