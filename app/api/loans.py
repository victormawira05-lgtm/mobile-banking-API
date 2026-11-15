from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()

class AffordabilityRequest(BaseModel):
    income: float = Field(2500, example=2500, description="Monthly income KES")
    expenses: float = Field(1500, example=1500, description="Monthly expenses KES")
    loan_amount: float = Field(500, example=500, description="Loan requested - 500 KES demo")
    loan_purpose: Optional[str] = Field("airtime", example="airtime", description="airtime, school, business")
    existing_debt: float = Field(0, example=0, description="Existing debt")

    class Config:
        json_schema_extra = {
            "example": {
                "income": 2500,
                "expenses": 1500,
                "loan_amount": 500,
                "loan_purpose": "airtime",
                "existing_debt": 0
            }
        }

@router.post("/affordability-check", summary="Check Affordability", description="Check if 500 KES loan is affordable")
def affordability_check(req: AffordabilityRequest):
    disposable = req.income - req.expenses - req.existing_debt
    affordability_ratio = disposable / req.loan_amount if req.loan_amount > 0 else 0
    dti = (req.existing_debt + req.expenses) / req.income if req.income > 0 else 1
    
    if disposable >= req.loan_amount * 1.5 and dti <= 0.4:
        decision = "approve"
        reason = f"Affordable: KES {disposable} disposable covers KES {req.loan_amount}"
        risk_score = 0.15
    else:
        decision = "decline"
        reason = f"Not affordable: disposable KES {disposable} low"
        risk_score = 0.75

    return {
        "decision": decision,
        "affordability_ratio": round(affordability_ratio, 2),
        "risk_score": risk_score,
        "disposable_income": disposable,
        "dti_ratio": round(dti, 2),
        "loan_amount": req.loan_amount,
        "currency": "KES",
        "reason": reason
    }

@router.get("/")
def list_loans():
    return {"message": "Loans API - Kenya"}
