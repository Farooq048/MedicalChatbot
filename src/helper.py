# Import library for extracting text from PDFs
import pdfplumber

# Import LangChain text splitter for chunking
from langchain.text_splitter import RecursiveCharacterTextSplitter


# -------------------------------
# PDF Text Extraction
# -------------------------------

def load_pdf(file):
    # Initialize empty string to store PDF text
    text = ""

    # Open the PDF file
    with pdfplumber.open(file) as pdf:

        # Loop through each page in the PDF
        for page in pdf.pages:

            # Extract text from the page
            page_text = page.extract_text()

            # Only add text if page is not empty
            if page_text:
                text += page_text + "\n"

    # Return full extracted text
    return text


# -------------------------------
# Text Chunking
# -------------------------------

def split_text(text):
    # Create text splitter with chunk size and overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Number of characters per chunk
        chunk_overlap=100     # Overlap to preserve context
    )

    # Split text into chunks and return
    return splitter.split_text(text)
