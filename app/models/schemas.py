from pydantic import BaseModel, Field

class LoanRequest(BaseModel):
    income: float = Field(..., gt=0, example=25000)
    existing_loans: float = Field(..., ge=0, example=5000)
    requested_amount: float = Field(..., gt=0, example=500)

class AffordabilityResponse(BaseModel):
    decision: str  # approve | review | deny
    affordable_ratio: float
    max_affordable: int
    requested_amount: float
    currency: str = "KES"
    reason: str
