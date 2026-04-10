from app.schemas.chat_schemas import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from langchain_pinecone import PineconeVectorStore

def retrieve_docs(state: ChatState) -> dict:
    vectorstore = state.get("vectorstore")
    
    # If starting a pure chat without uploading a file, vectorstore won't be in state yet.
    if not vectorstore:
        from app.services.services_rag import embeddings
        embeddings_model = state.get("embeddings_model")
        if not embeddings_model:
            embeddings_model = embeddings(state)["embeddings_model"]
        
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name="insurance-assistant-index", 
            embedding=embeddings_model
        )

    query = state.get("message")
    
    _agent_debug_log(
        hypothesis_id="H4",
        location="services_pinecone.retrieve_docs",
        message="Starting retrieve docs",
        data={"query": query},
    )
    
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    docs_content = [doc.page_content for doc in retrieved_docs]
    return {"retrieved_docs": docs_content}