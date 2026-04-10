from app.schemas.chat_schemas import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from langchain_pinecone import PineconeVectorStore

def pinecone_vector_store(state: ChatState) -> dict:
    embeddings_model = state.get("embeddings_model")
    list_chunks = state.get("list_chunks")
    
    _agent_debug_log(
        hypothesis_id="H4",
        location="services_pinecone.pinecone_vector_store",
        message="Starting pinecone vector store creation",
        data={"chunks": len(list_chunks)},
    )
    
    vectorstore = PineconeVectorStore.from_documents(
        documents=list_chunks,
        embedding=embeddings_model,
        index_name="insurance-assistant-index",
    )
    return {"vectorstore": vectorstore}

