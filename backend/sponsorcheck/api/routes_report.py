from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from sponsorcheck.reports.store import get_report_store
from sponsorcheck.reports.pdf_generator import generate_pdf

router = APIRouter()

class ReportRequest(BaseModel):
    report_id: str

@router.post("")
async def create_report(request: ReportRequest):
    data = get_report_store().get(request.report_id)
    if not data:
        raise HTTPException(status_code=404, detail="Report data not found.")
    return {"report_id": request.report_id, "status": "ready"}

@router.get("/{report_id}.pdf")
async def get_pdf_report(report_id: str):
    data = get_report_store().get(report_id)
    if not data:
        raise HTTPException(status_code=404, detail="Report data not found.")
        
    pdf_bytes = generate_pdf(data)
    
    return Response(content=pdf_bytes, media_type="application/pdf")
