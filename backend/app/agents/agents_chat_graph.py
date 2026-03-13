from dotenv import load_dotenv
from app.agents.agents_state import ChatState
from app.agents.agents_debug_log import _agent_debug_log
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in insurance. You are given a question and a context. Answer the question based on the context. If the answer is not in the context, say that you cannot answer the question. Do not answer any other question. Do not make up any information. write a short structured report (a few paragraphs) on the topic. Use only the information provided."),
    ("user", "question: {question}"),
])


def generate_reply(state: ChatState) -> dict:

    question = state.get("message", "no message found")
    print(f"--- Processing Query: {question} ---")
    context = "\n\n".join(state.get("retrieved_docs", []))
    if not question:
        return {"answer": "no answer found"}

    _agent_debug_log(
        hypothesis_id="H4",
        location="agents_chat_graph.generate_reply",
        message="Starting generate reply",
        data={"query": question, "context": context},
    )

    chain = SYSTEM_PROMPT | llm
    response = chain.invoke({"question": question, "context": context})

    return {"answer": response.content}