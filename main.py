# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from utils import extract_text_from_pdf, extract_text_from_docx, add_document_to_db, query_documents
import uuid
import os

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",  
]

# Apply CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve the HTML file on the root route"""
    return FileResponse("static/index.html")


@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    """Endpoint to ingest a document and store its embeddings."""
    doc_id = str(uuid.uuid4())
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True) 
    file_path = f"{temp_dir}/{doc_id}_{file.filename}"

    try:
        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        print(f"File saved to: {file_path}")  # Log the saved file path
        
        # Extract text based on file extension
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            text = open(file_path, "r").read()  # For TXT files

        add_document_to_db(text, doc_id)
        return {"message": "Document ingested successfully", "doc_id": doc_id}

    except Exception as e:
        print(f"Error during document ingestion: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Failed to process file", "error": str(e)})
    
    finally:
        os.remove(file_path) 


@app.get("/query")
async def query_documents_endpoint(query: str):
    """Endpoint to query documents based on similarity."""
    try:
        results = query_documents(query)  
        if results:
            return {"query_results": results}
        else:
            return {"message": "No results found for the query"}
    except Exception as e:
        print(f"Error during query: {e}")
        return JSONResponse(status_code=500, content={"message": "Query failed"})
