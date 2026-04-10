from app.schemas.chat_schemas import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from app.models.models_llm import llm, SYSTEM_PROMPT


def generate_reply(state: ChatState) -> dict:

    question = state.get("message", "no message found")
    print(f"--- Processing Query: {question} ---")
    
    # Defensively extract string content
    raw_docs = state.get("retrieved_docs", [])
    print(f"--- Retrieved Docs: {raw_docs} ---")
    if raw_docs:
        docs_strings = []
        for doc in raw_docs:
            if hasattr(doc, "page_content"):
                docs_strings.append(doc.page_content)
            else:
                docs_strings.append(str(doc))
                
        context = "\n\n".join(docs_strings)
    else:
        context = "no context found"

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
