from app.agents.agents_state import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

def embeddings(state: ChatState):
    _agent_debug_log(
        hypothesis_id="H4",
        location="services_embedings.embeddings",
        message="Starting embeddings creation",
        data={"chunks": len(state.get("list_chunks", []))},
    )

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name)

    return {"embeddings_model": embeddings_model}