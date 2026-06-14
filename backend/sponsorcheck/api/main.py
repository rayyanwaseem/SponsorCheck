from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sponsorcheck.api.routes_classify import router as classify_router
from sponsorcheck.api.routes_salary import router as salary_router
from sponsorcheck.api.routes_data import router as data_router
from sponsorcheck.api.routes_report import router as report_router

app = FastAPI(title="SponsorCheck API", description="API for UK Skilled Worker SOC classification and salary checks")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(classify_router, prefix="/api", tags=["Classify"])
app.include_router(salary_router, prefix="/api/salary", tags=["Salary"])
app.include_router(data_router, prefix="/api/data", tags=["Data"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
