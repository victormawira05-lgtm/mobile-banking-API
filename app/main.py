from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.loans import router as loans_router

app = FastAPI(title="Mobile Banking API - 500 KES Demo", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loans_router, prefix="/v1/loans", tags=["Loans"])

@app.get("/", tags=["Root"])
def root():
    return {"status": "ok", "message": "Mobile Banking API running", "docs": "/docs"}
