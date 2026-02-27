import os
import json
import time
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# region agent log
def _agent_debug_log(
    hypothesis_id: str,
    location: str,
    message: str,
    data: dict | None = None,
    run_id: str = "pre-fix-1",
) -> None:
    """
    Lightweight debug logger for this AI-assisted debug session.
    Writes NDJSON lines to the session log file without affecting main flow.
    """
    try:
        log_obj = {
            "sessionId": "9f7496",
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000),
        }
        log_path = Path(__file__).resolve().parents[3] / "debug" / "debug-9f7496.log"
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log_obj) + "\n")
    except Exception:
        # Never allow logging failures to break the main processing flow.
        pass


# endregion


def load_docs(policies_path: Path | None = None) -> list:
    """
    Load all PDF policy documents and attach their source filename in metadata.

    Returns a flat list of LangChain Document objects.
    """
    if policies_path is None:
        # backend/data/policies
        policies_path = (
            Path(__file__).resolve().parent.parent.parent / "data" / "policies"
        )

    exists = policies_path.exists()
    _agent_debug_log(
        hypothesis_id="H1",
        location="file_schema.load_docs",
        message="Policies path existence check",
        data={"policies_path": str(policies_path), "exists": exists},
    )

    if not exists:
        raise FileNotFoundError(f"Policies directory not found: {policies_path}")

    all_docs: list = []

    for path in sorted(policies_path.glob("*.pdf")):
        loader = PyPDFLoader(str(path))
        docs = loader.load()

        _agent_debug_log(
            hypothesis_id="H3",
            location="file_schema.load_docs",
            message="Loaded PDF file",
            data={"filename": path.name, "docs_in_file": len(docs)},
        )

        for doc in docs:
            path_array = path.name.split("_")

            _agent_debug_log(
                hypothesis_id="H2",
                location="file_schema.load_docs",
                message="Parsed policy filename",
                data={
                    "filename": path.name,
                    "parts": path_array,
                    "parts_len": len(path_array),
                },
            )

            doc.metadata["policy_name"] = path.name
            doc.metadata["document_type"] = path_array[1].strip()
            doc.metadata["category"] = path_array[0].strip()

        # extend once per file; keep list flat
        all_docs.extend(docs)

    _agent_debug_log(
        hypothesis_id="H3",
        location="file_schema.load_docs",
        message="Total documents loaded",
        data={"total_docs": len(all_docs)},
    )

    return all_docs



def create_chunks(all_docs: list) -> list:
    """
    Split documents into smaller chunks for downstream processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    list_chunks = text_splitter.split_documents(all_docs)

    _agent_debug_log(
        hypothesis_id="H3",
        location="file_schema.create_chunks",
        message="Chunks created from documents",
        data={"total_chunks": len(list_chunks)},
    )

    print(f"Total chunks created: {len(list_chunks)}")
    return list_chunks



def embeddings(list_chunks: list):
    _agent_debug_log(
        hypothesis_id="H4",
        location="file_schema.embeddings",
        message="Starting embeddings creation",
        data={"chunks": len(list_chunks)},
    )

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name)

    # 2. Embed and Store in a Vector Database
    # .from_documents handles extracting page_content AND preserving metadata
    # vectorstore = FAISS.from_documents(list_chunks, embeddings_model)
    vectorstore = PineconeVectorStore.from_documents(
        documents=list_chunks,
        embedding=embeddings_model,
        index_name="insurance-assistant-index",
    )

    # 3. Test a search
    query = "What is the premium for Car Insurance Gold?"
    docs = vectorstore.similarity_search(query, k=1)

    _agent_debug_log(
        hypothesis_id="H5",
        location="file_schema.embeddings",
        message="Similarity search completed",
        data={"query": query, "results": len(docs), "has_first": bool(docs)},
    )

    print(f"Result: {docs[0].page_content}")
    print(f"Source Policy: {docs[0].metadata['policy_name']}")



if __name__ == "__main__":
    all_docs = load_docs()
    list_chunks = create_chunks(all_docs)
    embeddings(list_chunks)

