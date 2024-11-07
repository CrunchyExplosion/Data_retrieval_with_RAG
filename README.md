# Generative AI Document Ingestion & Querying API

![image](https://github.com/user-attachments/assets/172733f9-b491-47f4-981c-6f0a571f641d)


## Overview
This project provides a FastAPI application that allows users to upload documents, process and store them in ChromaDB, and query the stored documents based on similarity to a user’s input. It supports PDF, DOCX, and TXT file formats, extracts text from them, and uses embeddings for querying.

The core functionality includes:
- Document ingestion and text extraction from various formats.
- Document embedding and storage in ChromaDB.
- Efficient querying of stored documents using semantic similarity.

## Technologies Used
- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.
- ChromaDB: A database for storing document embeddings for fast similarity searches.
- Sentence-Transformers: A library to compute sentence embeddings from text.
- PDFPlumber: A Python library to extract text from PDF files.
- python-docx: A Python library to extract text from DOCX files.
- Pydantic: Data validation and settings management using Python type annotations.
- Uvicorn: An ASGI server for FastAPI application.

## Project Structure
```
.
├── main.py                    # FastAPI app definition
├── utils.py                   # Helper functions for text extraction, document embedding, etc.
├── static/
│   └── index.html             # Frontend HTML for querying documents
├── temp_files/                # Temporary directory for file storage during ingestion
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (optional)
└── README.md                  # Project documentation

```

# API Endpoints
1. GET /
Description:
- Serves the HTML frontend (index.html) for interacting with the API.
Response:
- Returns the HTML file for the frontend.

2. POST /ingest
Description:
- Upload a document (PDF, DOCX, or TXT) for ingestion.
- Extracts the text from the document and stores it in ChromaDB.
Parameters:
- file: A file upload input (PDF, DOCX, or TXT).

Request Example:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/ingest' \
  -F 'file=@your_document.pdf'

```
Response
```
{
  "message": "Document ingested successfully",
  "doc_id": "1234-5678-abcd"
}
```

3. GET /query
Description:
- Query the database to find documents similar to the input text.
Parameters:
- query: The query text for searching similar documents.
Request Example:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/query?query=machine%20learning'
```
Response:
```
{
  "query_results": [
    "Document 1 content...",
    "Document 2 content..."
  ]
}

```
If no results are found:
```
{
  "message": "No results found for the query"
}
```
-----------------------------------------------------------------------------------------------

# Core Functions
Core Functions
## 1. extract_text_from_pdf(file_path)
- Description: Extracts text from a PDF document.
- Parameters: file_path (str) – The path to the PDF file.
- Returns: Extracted text (str).

## 2. extract_text_from_docx(file_path)
- Description: Extracts text from a DOCX document.
- Parameters: file_path (str) – The path to the DOCX file.
- Returns: Extracted text (str).
  
## 3. embed_text(text)
- Description: Converts text to embeddings using a pre-trained model.
- Parameters: text (str) – The input text to be embedded.
- Returns: Embedding (list of floats).

## 4. add_document_to_db(text, doc_id, chunk_size=500)
- Description: Adds a document's embeddings to ChromaDB.
- Parameters:
  - text (str) – The extracted text.
  - doc_id (str) – The unique identifier for the document.
  - chunk_size (int) – Size of text chunks to break the document into (default: 500).
- Returns: None.

## 5. query_documents(query_text, top_k=5)
- Description: Queries ChromaDB for documents similar to the input query.
- Parameters:
  - query_text (str) – The query text.
  - top_k (int) – The number of results to return (default: 5).
- Returns: A list of documents that match the query text.

  --------------------------------------------------------------------------------------
# Setup and Installation

## 1. Clone the Repository:
```
git clone https://github.com/CrunchyExplosion/Data_retrieval_with_RAG.git
cd Data_retrieval_with_RAG
```

## 2. Set Up Virtual Environment:
Ensure that you have Python 3.7+ installed and version less than 3.11. Create a virtual environment (optional) and install dependencies
Create a .env file in the root directory for environment variables like COLLECTION_NAME or TEMP_DIR.
```
pip install virtualenv
virtualenv myenv
.\myenv\Source\Activate
```

## 3. Install Dependencies:
```
pip install -r requirements.txt
```

## 4. Run the Application:
To run the FastAPI application, use Uvicorn:

```
uvicorn main:app --reload
```
The application will be running on http://127.0.0.1:8000/.

----------------------------------------------------------------------------------------

# Frontend Interface
The frontend consists of a basic HTML interface located at static/index.html. It allows users to:

- Upload a document.
- Query the documents for relevant results.

--------------------------------------------------------------------------------------------

# Limitations
- The current document processing pipeline supports PDF, DOCX, and TXT files. Files that don’t fall into these categories will be ignored.

- For large documents, the chunking method may need refinement, depending on specific use cases.

-----------------------------------------------------------------------------------------------

# Possible Improvements
## - Advanced Querying: Add support for advanced filtering (e.g., metadata, dates).
## - Document Chunking: Implement better chunking strategies, such as splitting documents by paragraphs or sections.
## - Error Handling: Add more detailed error handling and validation, especially for file formats.
## - User Authentication: Add user authentication for private document ingestion and querying.
## - Frontend Enhancements: Improve the frontend to display results in a more user-friendly format.

---------------------------------------------------------------------------------------------

Developed By - Apoorv Sharma
Thanks for checking out this Repository
