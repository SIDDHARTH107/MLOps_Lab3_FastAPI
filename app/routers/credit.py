from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from app.models.schemas import (
    CreditAssessmentRequest, CreditAssessmentResponse,
    CreditExplanation, ImprovementRoadmap
)
from app.services.credit_engine import CreditScoringEngine
from app.services.explainer import CreditExplainer

# This is the front door (or the interface) to my application. This file uses FastAPI to actually connect those features to the outside world so a website or mobile app can use them.

router = APIRouter(prefix="/api/v1/credit", tags=["Credit Assessment"])

# Initializing services
scoring_engine = CreditScoringEngine()
explainer = CreditExplainer()

@router.post("/assess", response_model=CreditAssessmentResponse)
async def assess_credit(request: CreditAssessmentRequest):
    """
    Comprehensive credit assessment with explainable AI
    
    This endpoint analyzes credit profile and provides:
    - Credit score with component breakdown
    - Detailed explanations for score factors
    - Actionable improvement suggestions
    - Lending recommendations
    """
    try:
        # Calculating comprehensive score
        final_score, component_scores = scoring_engine.calculate_comprehensive_score(
            request.applicant,
            request.credit_history,
            request.employment
        )
        
        # Generating explanations
        positive_factors, negative_factors, neutral_factors = explainer.generate_factor_explanations(
            component_scores,
            request.applicant,
            request.credit_history,
            request.employment
        )
        
        # Generating improvement suggestions
        improvement_suggestions = explainer.generate_improvement_suggestions(
            component_scores,
            request.applicant,
            request.credit_history,
            final_score
        )
        
        # Determining risk and approval probability
        risk_category = scoring_engine.determine_risk_category(final_score)
        approval_probability = scoring_engine.calculate_approval_probability(final_score)
        
        # Lending decision logic
        lending_decision, recommended_amount, recommended_rate, conditions = _make_lending_decision(
            final_score,
            request.requested_loan_amount,
            request.applicant.monthly_income,
            request.credit_history.loan_emi
        )
        
        # Creating explanation object
        explanation = CreditExplanation(
            score=final_score,
            risk_category=risk_category,
            approval_probability=approval_probability,
            top_positive_factors=positive_factors[:3],
            top_negative_factors=negative_factors[:3],
            neutral_factors=neutral_factors,
            improvement_suggestions=improvement_suggestions,
            score_breakdown={k: v['weighted_score'] for k, v in component_scores.items()}
        )
        
        # Creating response
        response = CreditAssessmentResponse(
            request_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            applicant_name=request.applicant.name,
            final_score=final_score,
            explanation=explanation,
            lending_decision=lending_decision,
            recommended_loan_amount=recommended_amount,
            recommended_interest_rate=recommended_rate,
            conditions=conditions
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")

@router.get("/improvement-roadmap")
async def get_improvement_roadmap(current_score: int, target_score: int = 750):
    """
    Generate a month-by-month improvement roadmap
    
    Shows specific actions to take each month to reach target score
    """
    if current_score >= target_score:
        raise HTTPException(
            status_code=400, 
            detail="Current score already meets or exceeds target"
        )
    
    if target_score > 900 or current_score < 300:
        raise HTTPException(status_code=400, detail="Invalid score range")
    
    # Generating roadmap
    score_gap = target_score - current_score
    estimated_months = max(6, int(score_gap / 10))  # ~10 points per month improvement
    
    milestones = []
    months_passed = 0
    current_projected_score = current_score
    
    # Month 1-2: Immediate actions
    milestones.append({
        "month": 1,
        "action": "Pay down credit cards to below 30% utilization",
        "expected_score_gain": 15,
        "projected_score": current_projected_score + 15
    })
    current_projected_score += 15
    
    milestones.append({
        "month": 2,
        "action": "Ensure all payments are on-time",
        "expected_score_gain": 10,
        "projected_score": current_projected_score + 10
    })
    current_projected_score += 10
    
    # Month 3-6: Sustained behavior
    for month in range(3, min(7, estimated_months + 1)):
        milestones.append({
            "month": month,
            "action": "Continue perfect payment record",
            "expected_score_gain": 8,
            "projected_score": min(current_projected_score + 8, target_score)
        })
        current_projected_score = min(current_projected_score + 8, target_score)
        
        if current_projected_score >= target_score:
            break
    
    # Remaining months: Natural aging
    while current_projected_score < target_score and len(milestones) < estimated_months:
        month_num = len(milestones) + 1
        gain = min(5, target_score - current_projected_score)
        milestones.append({
            "month": month_num,
            "action": "Account age increases naturally",
            "expected_score_gain": gain,
            "projected_score": min(current_projected_score + gain, target_score)
        })
        current_projected_score = min(current_projected_score + gain, target_score)
    
    roadmap = ImprovementRoadmap(
        current_score=current_score,
        target_score=target_score,
        estimated_timeline_months=len(milestones),
        monthly_milestones=milestones,
        total_expected_improvement=target_score - current_score
    )
    
    return roadmap

def _make_lending_decision(
    score: int,
    requested_amount: float,
    monthly_income: float,
    current_emi: float
) -> tuple:
    """Make lending decision based on score and financials"""
    
    # Calculating max affordable EMI (40% of income rule)
    max_emi = monthly_income * 0.40
    available_emi = max_emi - current_emi
    
    conditions = []
    
    if score >= 750:
        decision = "Approve"
        recommended_amount = min(requested_amount, monthly_income * 60)  # 60x monthly income
        recommended_rate = 10.5
        conditions = ["Standard terms apply", "Pre-approved for premium rate"]
        
    elif score >= 700:
        decision = "Approve"
        recommended_amount = min(requested_amount * 0.9, monthly_income * 50)
        recommended_rate = 11.5
        conditions = ["Standard verification required", "Income proof mandatory"]
        
    elif score >= 650:
        decision = "Review Required"
        recommended_amount = min(requested_amount * 0.75, monthly_income * 40)
        recommended_rate = 13.0
        conditions = [
            "Additional documentation required",
            "Co-applicant may improve terms",
            "Consider secured loan for better rates"
        ]
        
    elif score >= 600:
        decision = "Conditional Approval"
        recommended_amount = min(requested_amount * 0.50, monthly_income * 30)
        recommended_rate = 15.0
        conditions = [
            "Co-applicant required",
            "Collateral mandatory",
            "Higher processing fees apply"
        ]
        
    else:
        decision = "Reject"
        recommended_amount = None
        recommended_rate = None
        conditions = [
            "Score too low for approval",
            "Focus on improving credit score",
            "Consider secured credit products",
            f"Re-apply after score reaches 600+"
        ]
    
    return decision, recommended_amount, recommended_rate, conditions

# This file (the Router) is the boss. It stands at the front desk, receives applications from the internet, passes them to your engine and explainer to do the hard work, makes a final banking decision on the loan, and hands the complete report back to the customer.
