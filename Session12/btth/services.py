from fastapi import HTTPException
from models import DocumentModel, DocumentCreate
 
 # Lấy tất cả tài liệu
def get_all_documents(db):
    documents = db.query(DocumentModel).all()
    return {
        "message": "Đã lấy toàn bộ tài liệu",
        "data": documents
    }
    
# THêm tài liệu
def add_document(document: DocumentCreate, db):
    new_document = DocumentModel (
        title = document.title,
        subject = document.subject,
        document_type = document.document_type,
        file_url = document.file_url
    )
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return {
        "message": "Thêm tài liệu thành công",
        "data": new_document
    }
#Xoá tìa liệu
def delete_document_service(document_id:int, db):
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    if document is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy tài liệu cần xoá"
        )
    db.delete(document)
    db.commit()
    return {
        "message": "Xoá tài liệu thành công",
        "data": document
    }