from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import DocumentCreate
from services import get_all_documents, add_document, delete_document_service

app = FastAPI()

@app.get("/documents")
def get_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)

@app.post("/documents")
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    return add_document(document, db)

@app.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session=Depends(get_db)):
    return delete_document_service(document_id, db)