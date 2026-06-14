import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import pypdf
from docx import Document

router = APIRouter()

class ExtractResponse(BaseModel):
    text: str
    filename: str

@router.post("/extract", response_model=ExtractResponse)
async def extract_text(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = await file.read()
    
    text = ""
    try:
        if filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        elif filename.endswith(".pdf"):
            pdf_file = io.BytesIO(content)
            reader = pypdf.PdfReader(pdf_file)
            text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif filename.endswith(".docx"):
            docx_file = io.BytesIO(content)
            doc = Document(docx_file)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload TXT, PDF, or DOCX.")
            
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the file.")
            
        return ExtractResponse(text=text.strip(), filename=file.filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
