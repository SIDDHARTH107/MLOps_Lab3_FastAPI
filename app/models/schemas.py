from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class ApplicantInfo(BaseModel):
    """Basic applicant information"""
    name: str = Field(..., example="Amit Kumar")
    pan: str = Field(..., example="ABCDE1234F")
    phone: str = Field(..., example="+919876543210")
    email: str = Field(..., example="amit@email.com")
    age: int = Field(..., ge=18, le=100, example=32)
    monthly_income: float = Field(..., gt=0, example=50000)

    @validator('pan')
    def validate_pan(cls, v):
        """Validate PAN format"""
        import re
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', v):
            raise ValueError('Invalid PAN format')
        return v.upper()

class CreditHistory(BaseModel):
    """Credit history details"""
    cibil_score: int = Field(..., ge=300, le=900, example=720)
    credit_cards: int = Field(..., ge=0, example=3)
    total_credit_limit: float = Field(..., ge=0, example=500000)
    credit_utilization: float = Field(..., ge=0, le=100, example=35)
    active_loans: int = Field(..., ge=0, example=2)
    total_loan_amount: float = Field(..., ge=0, example=1000000)
    loan_emi: float = Field(..., ge=0, example=25000)
    credit_history_length_months: int = Field(..., ge=0, example=48)
    missed_payments_last_year: int = Field(..., ge=0, example=0)
    hard_inquiries_last_6_months: int = Field(..., ge=0, example=2)

class EmploymentInfo(BaseModel):
    """Employment details"""
    employment_type: str = Field(..., example="Salaried")
    job_stability_months: int = Field(..., ge=0, example=36)
    employer_type: str = Field(..., example="Private Sector")

class CreditAssessmentRequest(BaseModel):
    """Complete credit assessment request"""
    applicant: ApplicantInfo
    credit_history: CreditHistory
    employment: EmploymentInfo
    requested_loan_amount: float = Field(..., gt=0, example=500000)
    loan_purpose: str = Field(..., example="Personal Loan")

class CreditFactor(BaseModel):
    """Individual credit factor explanation"""
    factor: str
    current_value: str
    impact: str  # "Positive", "Negative", "Neutral"
    score_impact: int  # Points added/subtracted
    weight: str  # "High", "Medium", "Low"
    explanation: str

class ImprovementAction(BaseModel):
    """Actionable improvement suggestion"""
    action: str
    expected_impact: int  # Score points
    timeline: str
    difficulty: str  # "Easy", "Medium", "Hard"
    priority: str  # "High", "Medium", "Low"

class CreditExplanation(BaseModel):
    """Detailed credit score explanation"""
    score: int
    risk_category: str  # "Low", "Medium", "High"
    approval_probability: float  # 0-100
    top_positive_factors: List[CreditFactor]
    top_negative_factors: List[CreditFactor]
    neutral_factors: List[CreditFactor]
    improvement_suggestions: List[ImprovementAction]
    score_breakdown: dict

class CreditAssessmentResponse(BaseModel):
    """Complete assessment response"""
    request_id: str
    timestamp: datetime
    applicant_name: str
    final_score: int
    explanation: CreditExplanation
    lending_decision: str  # "Approve", "Review", "Reject"
    recommended_loan_amount: Optional[float]
    recommended_interest_rate: Optional[float]
    conditions: List[str]

class ImprovementRoadmap(BaseModel):
    """Credit improvement roadmap"""
    current_score: int
    target_score: int
    estimated_timeline_months: int
    monthly_milestones: List[dict]
    total_expected_improvement: int
