from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mobile Banking API - 500 KES Demo", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class AffordabilityCheck(BaseModel):
    existing_debt: float = 0
    expenses: float = 1500
    income: float = 2500
    loan_amount: float = 500
    loan_purpose: str = "airtime"

@app.get("/")
def root():
    return {"service": "Mobile Banking API - 500 KES Demo", "status": "live", "docs": "/docs"}

@app.post("/v1/loans/affordability-check")
def check_affordability(req: AffordabilityCheck):
    # 500 KES Loan Logic
    disposable = req.income - req.expenses - req.existing_debt
    monthly_payment = req.loan_amount * 1.15  # 15% fee for 30 days
    
    # Affordability rules for 500 KES
    debt_to_income = (req.existing_debt + monthly_payment) / req.income if req.income > 0 else 1
    can_afford = disposable >= monthly_payment and debt_to_income <= 0.4
    
    reasons = []
    if disposable < monthly_payment:
        reasons.append(f"FAIL: Disposable {disposable} KES < payment {monthly_payment} KES")
    else:
        reasons.append(f"PASS: Disposable {disposable} KES >= payment {monthly_payment} KES")
    
    if debt_to_income > 0.4:
        reasons.append(f"FAIL: Debt-to-income {debt_to_income*100:.1f}% > 40% limit")
    else:
        reasons.append(f"PASS: Debt-to-income {debt_to_income*100:.1f}% within limit")

    if req.income < 2000:
        return {
            "loan_amount": req.loan_amount,
            "decision": "DENY",
            "affordable": False,
            "score": 20,
            "reasons": reasons + ["Hard DENY: Income < 2000 KES (CBK rule)"],
            "message": "500 KES loan DENIED - Income too low"
        }

    if can_afford:
        return {
            "loan_amount": req.loan_amount,
            "decision": "AWARD",
            "affordable": True,
            "score": 85,
            "approved_amount": req.loan_amount,
            "monthly_payment": monthly_payment,
            "disposable_income": disposable,
            "reasons": reasons,
            "message": "AWARD: 500 KES loan affordable - Disburse via M-Pesa"
        }
    else:
        return {
            "loan_amount": req.loan_amount,
            "decision": "DENY",
            "affordable": False,
            "score": 35,
            "approved_amount": 0,
            "monthly_payment": monthly_payment,
            "disposable_income": disposable,
            "reasons": reasons,
            "message": "DENY: 500 KES loan not affordable"
        }
