from app.core.config import settings
from app.models.schemas import LoanRequest, AffordabilityResponse

def check_affordability(payload: LoanRequest) -> AffordabilityResponse:
    disposable = payload.income - payload.existing_loans
    
    if disposable <= 0:
        return AffordabilityResponse(
            decision="deny",
            affordable_ratio=0.0,
            max_affordable=0,
            requested_amount=payload.requested_amount,
            reason="No disposable income after existing obligations"
        )

    max_affordable = disposable * settings.max_dti_ratio
    ratio = max_affordable / payload.requested_amount if payload.requested_amount else 0

    if ratio >= settings.min_approval_ratio:
        decision = "approve"
        reason = f"Affordable. Ratio {ratio:.2f} >= {settings.min_approval_ratio}"
    elif ratio >= 1.0:
        decision = "review"
        reason = f"Marginal. Manual review required. Ratio {ratio:.2f}"
    else:
        decision = "deny"
        reason = f"Not affordable. Ratio {ratio:.2f} < 1.0"

    return AffordabilityResponse(
        decision=decision,
        affordable_ratio=round(ratio, 2),
        max_affordable=int(max_affordable),
        requested_amount=payload.requested_amount,
        reason=reason
    )
