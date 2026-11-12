from fastapi import APIRouter
from app.models.schemas import LoanRequest, AffordabilityResponse
from app.services.affordability import check_affordability

router = APIRouter(prefix="/v1/loans", tags=["Loans"])

@router.post("/affordability-check", response_model=AffordabilityResponse, summary="Check Affordability")
def affordability_check(payload: LoanRequest):
    """
    Kenyan micro-loan compliance check.
    Used by your 500 KES Demo button.
    """
    return check_affordability(payload)
