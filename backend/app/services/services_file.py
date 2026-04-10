from pathlib import Path
from dotenv import load_dotenv
from app.schemas.chat_schemas import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def load_docs(state: ChatState) -> dict:
    """
    Load PDF policy documents. If file_path is in state, load only that file.
    Otherwise, load all PDFs from the default policies directory.
    """
    file_path = state.get("file_path")
    
    # Define default path if not loading a specific file or if path is not provided
    import os
    upload_dir_str = os.getenv("UPLOAD_DIR", "data/policies")
    project_root = Path(__file__).resolve().parent.parent.parent
    default_policies_path = project_root / upload_dir_str

    all_docs: list = []

    if file_path:
        # Load a single specific file
        path = Path(file_path)
        if not path.is_absolute():
             path = project_root / path
        
        file_paths = [path]
    else:
        # Load all from directory
        if not default_policies_path.exists():
            print(f"Policies directory not found: {default_policies_path}")
            return {"all_docs": []}
        file_paths = sorted(default_policies_path.glob("*.pdf"))

    _agent_debug_log(
        hypothesis_id="H1",
        location="services_file.load_docs",
        message="Starting document loading",
        data={"file_path_provided": bool(file_path), "files_found": len(file_paths)},
    )

    for path in file_paths:
        if not path.exists():
            continue

        try:
            loader = PyPDFLoader(str(path))
            docs = loader.load()
    
            _agent_debug_log(
                hypothesis_id="H3",
                location="services_file.load_docs",
                message="Loaded PDF file",
                data={"filename": path.name, "docs_in_file": len(docs)},
            )
    
            for doc in docs:
                # Metadata extraction with fallback for non-conforming filenames
                path_array = path.name.split("_")
                
                doc.metadata["policy_name"] = path.name
                if len(path_array) >= 2:
                    doc.metadata["category"] = path_array[0].strip()
                    doc.metadata["document_type"] = path_array[1].strip()
                else:
                    doc.metadata["category"] = "General"
                    doc.metadata["document_type"] = "Policy"
    
                _agent_debug_log(
                    hypothesis_id="H2",
                    location="services_file.load_docs",
                    message="Metadata extraction",
                    data={
                        "filename": path.name,
                        "category": doc.metadata["category"],
                        "document_type": doc.metadata["document_type"]
                    },
                )
    
            all_docs.extend(docs)
        except Exception as e:
            print(f"Error loading PDF {path}: {e}")
            _agent_debug_log(
                hypothesis_id="H3",
                location="services_file.load_docs",
                message=f"Error loading PDF {path.name}",
                data={"error": str(e)},
            )

    _agent_debug_log(
        hypothesis_id="H3",
        location="services_file.load_docs",
        message="Total documents loaded",
        data={"total_docs": len(all_docs)},
    )

    return {"all_docs": all_docs}



def create_chunks(state: ChatState) -> dict:
    """
    Split documents into smaller chunks for downstream processing.
    """
    all_docs = state.get("all_docs", [])
    if not all_docs:
        _agent_debug_log(
            hypothesis_id="H3",
            location="services_file.create_chunks",
            message="No documents to chunk",
            data={"all_docs_len": 0},
        )
        return {"list_chunks": []}

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    list_chunks = text_splitter.split_documents(all_docs)

    _agent_debug_log(
        hypothesis_id="H3",
        location="services_file.create_chunks",
        message="Chunks created from documents",
        data={"total_chunks": len(list_chunks)},
    )

    print(f"Total chunks created: {len(list_chunks)}")
    return {"list_chunks": list_chunks}



# if __name__ == "__main__":
#     all_docs = load_docs()
#     list_chunks = create_chunks(all_docs)
#     embeddings(list_chunks)

