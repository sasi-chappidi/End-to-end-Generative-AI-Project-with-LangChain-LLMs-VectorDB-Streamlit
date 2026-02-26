

# 📚 PDF Q&A Chatbot (Streamlit + Gemini + FAISS) — Full Detailed README

This project lets you **upload PDF files** and **ask questions** about them.  
It extracts PDF text, splits it into chunks, generates embeddings using **Gemini Embedding**, stores them in **FAISS**, retrieves the most relevant chunks for your question, and then uses **Gemini (generateContent)** to answer using only the PDF context.

✅ Built to work smoothly on **free quota** by indexing only **first N pages** (example: 20 pages).

---

## ✅ What This App Does (Flow)
1. Upload PDF(s) in Streamlit UI
2. Extract text from PDF pages using PyPDF2
3. Split the text into overlapping chunks
4. Create embeddings for each chunk (Gemini Embedding 001)
5. Store embeddings in FAISS vector store
6. When user asks a question:
   - Retrieve top-k relevant chunks from FAISS
   - Build a prompt with chat history + retrieved context
   - Call Gemini model to answer
7. Show answer + source chunks (for transparency)

---

## ✨ Features
- Upload one or multiple PDFs
- Works with large PDFs by indexing only limited pages (free-tier friendly)
- Conversational Q&A (keeps chat history)
- Retrieval-Augmented Generation (RAG)
- Shows sources used for answers
- Uses FAISS for fast similarity search

---

## 🧰 Tech Stack
- **Python**
- **Streamlit** (UI)
- **PyPDF2** (PDF text extraction)
- **LangChain Text Splitters** (chunking)
- **Gemini API** (LLM + embeddings)
- **FAISS** (vector database)

---

## 📁 Project Structure
End-to-end-Generative-AI-Project-with-LangChain-LLMs-VectorDB-Streamlit/
│
├── app.py
├── requirements.txt
├── setup.py (optional, only if using -e .)
├── .env (API key stored here, NOT committed)
│
└── src/
├── init.py
└── helper.py

---

## ✅ Prerequisites
- Python 3.9+ (recommended 3.10)
- Conda (optional but recommended)
- Gemini API key (Google AI Studio)

---

## 🔑 Setup Gemini API Key
1) Create API key from Google AI Studio  
2) Create `.env` file in project root (same folder as `app.py`)  
3) Add:
GOOGLE_API_KEY=YOUR_API_KEY_HERE

⚠️ **Never upload `.env` or your API key to GitHub**.  
If exposed, rotate/regenerate immediately.

---

## ✅ Installation

### Option 1: Using Conda (Recommended)
```bash
conda create -n geneai python=3.10 -y
conda activate geneai
pip install -r requirements.txt

Create a file named requirements.txt:

streamlit
python-dotenv
PyPDF2
faiss-cpu

langchain
langchain-community
langchain-text-splitters
langchain-google-genai
google-genai

If you have setup.py and want editable install, you can add -e .
If you don’t have setup/pyproject, don’t add it.

Run the Application

From project root:
streamlit run app.py
Then open in browser:
Local URL: http://localhost


Common Errors & Fixes
1) 429 RESOURCE_EXHAUSTED (Quota exceeded)

Reason: too many embedding requests per minute.
Fix:

Reduce max_pages

Increase chunk_size

Retry after 30–60 sec

2) 404 Model Not Found

Reason: wrong model name.
Fix: use exact model name from ListModels:

LLM: models/gemini-2.5-flash

Embeddings: models/gemini-embedding-001

3) Import Errors (LangChain changes)

Fix: keep this project’s code as-is, avoid chains/memory imports.


---

## 👤 Author

**Sasi Chappidi**  
Master’s Student | Generative AI / LLM Systems | RAG | ML Engineering  

- 📍 St. Louis, MO, USA  
- 📧 Email: csasi099@gmail.com  
- 🔗 LinkedIn: https://www.linkedin.com/in/sasi-chappidi  
- 💻 GitHub: https://github.com/sasi-chappidi  

---