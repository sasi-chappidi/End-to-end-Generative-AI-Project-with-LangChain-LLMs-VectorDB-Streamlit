import streamlit as st
from src.helper import get_text_chunks, get_pdf_text, get_vector_store, get_conversation_chain


def main():
    st.set_page_config(page_title="Information Retrieval System", page_icon="✨", layout="centered")
    st.header("Information Retrieval System")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload PDF files", accept_multiple_files=True, type=["pdf"])

        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
            else:
                with st.spinner("Processing PDF files..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store)
                    st.session_state.chat_history = []  # reset history for new PDFs
                st.success("PDF files processed successfully!")

    st.divider()

    user_question = st.text_input("Ask a question about your PDFs:")

    if user_question and st.session_state.conversation:
        result = st.session_state.conversation({
            "question": user_question,
            "chat_history": st.session_state.chat_history
        })

        answer = result.get("answer", "")
        st.subheader("Answer")
        st.write(answer)

        st.session_state.chat_history.append((user_question, answer))

        with st.expander("Sources"):
            for i, doc in enumerate(result.get("source_documents", []), start=1):
                st.markdown(f"**Source {i}:**")
                st.write(doc.page_content[:1200])

    elif user_question and not st.session_state.conversation:
        st.info("Upload PDFs and click **Submit & Process** first.")


if __name__ == "__main__":
    main()