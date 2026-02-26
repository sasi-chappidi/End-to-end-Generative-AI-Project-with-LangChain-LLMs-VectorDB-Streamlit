import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Put it in .env as GOOGLE_API_KEY=...")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def get_pdf_text(pdf_docs) -> str:
    text = ""
    for pdf in pdf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    return text


def get_text_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 150):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.create_documents([text])


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return FAISS.from_documents(text_chunks, embedding=embeddings)


class SimpleConversationalRAG:
    def __init__(self, vector_store, k: int = 4):
        self.vector_store = vector_store
        self.retriever = vector_store.as_retriever(search_kwargs={"k": k})
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

    def __call__(self, inputs: dict):
        question = inputs.get("question", "")
        chat_history = inputs.get("chat_history", [])

        # retrieve docs (support both APIs)
        try:
            docs = self.retriever.get_relevant_documents(question)
        except Exception:
            docs = self.retriever.invoke(question)

        context = "\n\n".join([d.page_content for d in docs])

        history_text = ""
        for q, a in chat_history[-6:]:
            history_text += f"User: {q}\nAssistant: {a}\n"

        prompt = f"""
You are a helpful assistant. Answer using ONLY the provided context.
If the answer is not in the context, say: "I don't have enough information from the uploaded PDFs."

Chat history:
{history_text}

Context:
{context}

Question: {question}
Answer:
""".strip()

        resp = self.llm.invoke(prompt)
        answer = getattr(resp, "content", str(resp))

        return {"answer": answer, "source_documents": docs}


def get_conversation_chain(vector_store):
    # keep same function name your app.py imports
    return SimpleConversationalRAG(vector_store)