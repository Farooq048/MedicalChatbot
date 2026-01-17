# Import Streamlit for building the web interface
import streamlit as st

# Import PDF processing functions
from src.helper import load_pdf, split_text

# Import Pinecone storage function
from src.vector_store import store_documents

# Import RAG-based question answering function
from src.qa import ask_question


# -------------------------------
# Page Configuration
# -------------------------------

# Configure page title and layout
st.set_page_config(
    page_title="MediBot",
    layout="wide"
)


# -------------------------------
# Title & Disclaimer
# -------------------------------

# Display application title
st.title("🩺 MediBot – Medical PDF Chatbot")

# Medical disclaimer for safety and compliance
st.markdown(
    "**Disclaimer:** This tool is for educational purposes only "
    "and does not provide medical advice."
)


# -------------------------------
# PDF Upload Section
# -------------------------------

# Create file uploader that accepts only PDF files
uploaded_file = st.file_uploader(
    "Upload Medical PDF",
    type=["pdf"]
)


# -------------------------------
# PDF Processing Logic
# -------------------------------

# Run this block only after a PDF is uploaded
if uploaded_file:

    # Show loading spinner while processing
    with st.spinner("Processing PDF..."):

        # Extract text from the uploaded PDF
        text = load_pdf(uploaded_file)

        # Split extracted text into chunks
        chunks = split_text(text)

        # Convert chunks into embeddings and store in Pinecone
        store_documents(chunks)

    # Show success message
    st.success("PDF indexed successfully!")


# -------------------------------
# User Query Input
# -------------------------------

# Input box for user to ask a question
query = st.text_input(
    "Ask a question from the document"
)


# -------------------------------
# Question Answering Section
# -------------------------------

# Run only if user enters a question
if query:

    # Show spinner while searching
    with st.spinner("Searching..."):

        # Call RAG pipeline:
        # Embed query → retrieve relevant chunks → generate answer
        answer, sources = ask_question(query)

    # Display answer
    st.subheader("Answer")
    st.write(answer)

    # Display retrieved source text
    st.subheader("Source Context")
    for src in sources:
        st.info(src)
