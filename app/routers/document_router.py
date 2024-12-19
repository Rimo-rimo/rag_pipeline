from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas import DocumentSummaryResponse
from app.config import settings
import os
from urllib.parse import unquote

router = APIRouter()

@router.get("/summary", response_model=DocumentSummaryResponse)
def get_document_summary(file_path: str = Query(..., description="Path to the document")):
    try:
        file_path = unquote(file_path)
        collection_name = file_path.split("/")[3]
        document_name = ".".join(file_path.split("/")[-1].split(".")[:-1])
        summarized_text_path = os.path.join(settings.summarized_document_path, collection_name, document_name+".txt")
        
        # print(summarized_text_path)
        with open(summarized_text_path, 'r', encoding='utf-8') as f:
            summary = f.read()
            
        return DocumentSummaryResponse(
                message="요약 텍스트를 성공적으로 반환했습니다.",
                data={
                    "file_path": file_path,
                    "summary": summary
                }
            )
        
    except:
        raise HTTPException(status_code=404, detail="Document not found")