import pdfplumber
import docx
from sentence_transformers import SentenceTransformer
from chromadb import Client
from fastapi import HTTPException

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize ChromaDB client
chroma_client = Client()

# Create or get an existing collection for storing documents
collection_name = "document_collection"
try:
    collection = chroma_client.get_or_create_collection(collection_name)
except Exception as e:
    raise HTTPException(status_code=500, detail="Failed to initialize ChromaDB collection")

def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise

def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        raise

def embed_text(text):
    return model.encode(text).tolist()

def add_document_to_db(text, doc_id, chunk_size=500):
    try:
        chunks = chunk_document(text, chunk_size)
        
        embeddings = [embed_text(chunk) for chunk in chunks]
 
        collection.add(
            ids=[f"{doc_id}_{i}" for i in range(len(chunks))],  
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{"doc_id": doc_id}] * len(chunks) 
        )
    except Exception as e:
        print(f"Error adding document to DB: {e}")
        raise

def chunk_document(text, chunk_size=500):
    """Splits the document into smaller chunks."""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def query_documents(query_text, top_k=5):
    try:
        query_embedding = embed_text(query_text)  
        
        # Query the ChromaDB collection
        results = collection.query(
            query_embeddings=[query_embedding], 
            n_results=top_k 
        )
        

        if 'documents' in results:
            return results['documents'] 
        else:
            return [] 

    except Exception as e:
        print(f"Error during querying: {e}")
        raise HTTPException(status_code=500, detail="Error during querying")
