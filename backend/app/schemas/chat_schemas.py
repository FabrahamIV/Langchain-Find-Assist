from typing import TypedDict, Annotated

class ChatState(TypedDict, total=False):
    message: str
    conversation_id: str
    file_path: str
    list_chunks: list[str]
    all_docs: list
    embeddings_model: any
    vectorstore: any
    retrieved_docs: Annotated[list[str], lambda x, y: (x + y)[-5:]]
    answer: str