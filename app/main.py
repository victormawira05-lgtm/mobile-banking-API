from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import loans
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="One API to launch compliant micro-loans. Built for Kenya, M-Pesa ready.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loans.router)

@app.get("/")
def root():
    return {"message": "Mobile Banking API - 500 KES Demo Ready", "docs": "/docs"}
