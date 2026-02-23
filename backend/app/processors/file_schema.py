from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_pinecone import PineconeSparseVectorStore


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

    if not policies_path.exists():
        raise FileNotFoundError(f"Policies directory not found: {policies_path}")

    all_docs: list = []

    for path in sorted(policies_path.glob("*.pdf")):
        loader = PyPDFLoader(str(path))
        docs = loader.load()

        for doc in docs:
            path_array = path.name.split("_")
            doc.metadata["policy_name"] = path.name
            doc.metadata["document_type"] = path_array[1].strip()
            doc.metadata["category"] = path_array[0].strip()

        # extend once per file; keep list flat
        all_docs.extend(docs)

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
    print(f"Total chunks created: {len(list_chunks)}")
    return list_chunks



def embeddings(list_chunks: list):
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name)

    # 2. Embed and Store in a Vector Database
    # .from_documents handles extracting page_content AND preserving metadata
    # vectorstore = FAISS.from_documents(list_chunks, embeddings_model)
    vectorstore = PineconeSparseVectorStore.from_documents(
        documents=list_chunks,
        embedding=embeddings_model,
        index = "insurance-assistant-index"
    )

    # 3. Test a search
    query = "What is the premium for Car Insurance Gold?"
    docs = vectorstore.similarity_search(query, k=1)

    print(f"Result: {docs[0].page_content}")
    print(f"Source Policy: {docs[0].metadata['policy_name']}")



if __name__ == "__main__":
    all_docs = load_docs()
    list_chunks = create_chunks(all_docs)
    embeddings(list_chunks)

