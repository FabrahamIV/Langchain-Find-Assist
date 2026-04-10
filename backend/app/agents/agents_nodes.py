import os
from typing import Dict, Any, Literal
from app.schemas.chat_schemas import ChatState
from app.services.services_file import load_docs, create_chunks
from app.services.services_rag import embeddings
from app.services.services_pinecone import pinecone_vector_store
from app.services.services_retrieve_docs import retrieve_docs
from app.services.services_generate_reply import generate_reply


def process_file_node(state: ChatState) -> dict:
    """
    Node to process an uploaded file.
    Runs the file through the sequence of loading, chunking, embedding, 
    and storing into Pinecone vectorstore.
    """
    # 1. Load documents
    docs_result = load_docs(state)
    state.update(docs_result)
    
    # 2. Create chunks
    chunks_result = create_chunks(state)
    state.update(chunks_result)
    
    # 3. Initialize embeddings
    embeddings_result = embeddings(state)
    state.update(embeddings_result)
    
    # 4. Store in vectorstore
    vectorstore_result = pinecone_vector_store(state)
    
    return {
        **docs_result,
        **chunks_result,
        **embeddings_result,
        **vectorstore_result
    }

def retrieve_node(state: ChatState) -> dict:
    """
    Node to retrieve relevant documents based on the user's message.
    Requires a vectorstore in the state.
    """
    return retrieve_docs(state)

def reply_node(state: ChatState) -> dict:
    """
    Node to generate a reply using the Gemini LLM.
    Uses the agent's chat graph logic to provide an answer.
    """
    return generate_reply(state)

def route_based_on_file(state: ChatState) -> Literal["process_file_node", "retrieve_node"]:
    """
    Conditional routing: if a file_path is present in the state,
    route to the file processing node. Otherwise, skip to retrieval.
    """
    # If a file is attached to the state, perform file processing
    if state.get("file_path"):
        return "process_file_node"
    
    # Otherwise go straight to retrieve/reply
    return "retrieve_node"
