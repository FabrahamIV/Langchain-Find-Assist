from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

with open("app/prompt/System.txt", "r") as f:
    f_prompt = f.read()

SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", f_prompt),
    ("user", "question: {question}"),
])