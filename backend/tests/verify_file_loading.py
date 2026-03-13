import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_path))

from app.services.services_file import load_docs, create_chunks
from app.agents.agents_state import ChatState

def test_load_docs_directory():
    print("\n--- Testing load_docs (Default Directory) ---")
    state: ChatState = {}
    result = load_docs(state)
    docs = result.get("all_docs", [])
    print(f"Loaded {len(docs)} documents from directory.")
    if docs:
        print(f"First doc metadata: {docs[0].metadata}")
    return len(docs) > 0

def test_load_docs_specific_file():
    print("\n--- Testing load_docs (Specific File) ---")
    # Find a PDF in the policies dir to use as a test
    policies_path = Path(__file__).resolve().parent.parent / "data" / "policies"
    pdfs = list(policies_path.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in data/policies to test with.")
        return False
    
    test_pdf = pdfs[0]
    print(f"Testing with: {test_pdf}")
    state: ChatState = {"file_path": str(test_pdf)}
    result = load_docs(state)
    docs = result.get("all_docs", [])
    print(f"Loaded {len(docs)} documents from specific file.")
    
    # Verify only this file was loaded
    for doc in docs:
        if doc.metadata["policy_name"] != test_pdf.name:
            print(f"Error: Found document from another file: {doc.metadata['policy_name']}")
            return False
            
    print("Success: Only the specific file was loaded.")
    return len(docs) > 0

def test_chunking():
    print("\n--- Testing create_chunks ---")
    state: ChatState = {"all_docs": []} # To be populated
    # Assume we load something first
    load_result = load_docs({})
    state["all_docs"] = load_result["all_docs"]
    
    chunk_result = create_chunks(state)
    chunks = chunk_result.get("list_chunks", [])
    print(f"Created {len(chunks)} chunks.")
    return len(chunks) > 0

if __name__ == "__main__":
    s1 = test_load_docs_directory()
    s2 = test_load_docs_specific_file()
    s3 = test_chunking()
    
    if all([s1, s2, s3]):
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)
