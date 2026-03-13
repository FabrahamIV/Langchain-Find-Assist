from app.agents.agents_state import ChatState
from langchain_pinecone import PineconeVectorStore
from app.agents.agents_debug_log import _agent_debug_log

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

def retrieve_docs(state: ChatState) -> dict:
    vectorstore = state.get("vectorstore")
    query = state.get("message")
    
    _agent_debug_log(
        hypothesis_id="H4",
        location="services_pinecone.retrieve_docs",
        message="Starting retrieve docs",
        data={"query": query},
    )
    
    retrieved_docs = vectorstore.similarity_search(query, k=1)
    return {"retrieved_docs": retrieved_docs}