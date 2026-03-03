import numpy as np
from typing import Dict, Tuple
from app.models.schemas import CreditHistory, ApplicantInfo, EmploymentInfo

## Here, I am planning to build a scoring algorithm. It will look at seven different pieces of a person's financial life, scores each one individually, and then combines them to give a final "Credit Score" (between 300 and 900) and a risk assessment.

class CreditScoringEngine:
    """
    Credit scoring engine with explainable logic
    Based on standard credit risk assessment practices
    """
    
    def __init__(self):
        # Weight configuration for different factors
        self.weights = {
            'cibil_score': 0.30,
            'credit_utilization': 0.15,
            'payment_history': 0.20,
            'credit_history_length': 0.10,
            'hard_inquiries': 0.10,
            'debt_to_income': 0.10,
            'job_stability': 0.05
        }
    
    def calculate_comprehensive_score(
        self, 
        applicant: ApplicantInfo,
        credit_history: CreditHistory,
        employment: EmploymentInfo
    ) -> Tuple[int, Dict]:
        """
        Calculate comprehensive credit score with component breakdown
        
        Returns:
            Tuple of (final_score, component_scores_dict)
        """
        component_scores = {}
        
        # 1. Base CIBIL Score Component (Weight: 30%)
        cibil_component = self._score_cibil(credit_history.cibil_score)
        component_scores['cibil_score'] = {
            'raw_value': credit_history.cibil_score,
            'normalized_score': cibil_component,
            'weighted_score': cibil_component * self.weights['cibil_score'],
            'weight': self.weights['cibil_score']
        }
        
        # 2. Credit Utilization Component (Weight: 15%)
        utilization_component = self._score_credit_utilization(
            credit_history.credit_utilization
        )
        component_scores['credit_utilization'] = {
            'raw_value': credit_history.credit_utilization,
            'normalized_score': utilization_component,
            'weighted_score': utilization_component * self.weights['credit_utilization'],
            'weight': self.weights['credit_utilization']
        }
        
        # 3. Payment History Component (Weight: 20%)
        payment_component = self._score_payment_history(
            credit_history.missed_payments_last_year
        )
        component_scores['payment_history'] = {
            'raw_value': credit_history.missed_payments_last_year,
            'normalized_score': payment_component,
            'weighted_score': payment_component * self.weights['payment_history'],
            'weight': self.weights['payment_history']
        }
        
        # 4. Credit History Length Component (Weight: 10%)
        history_component = self._score_credit_history_length(
            credit_history.credit_history_length_months
        )
        component_scores['credit_history_length'] = {
            'raw_value': credit_history.credit_history_length_months,
            'normalized_score': history_component,
            'weighted_score': history_component * self.weights['credit_history_length'],
            'weight': self.weights['credit_history_length']
        }
        
        # 5. Hard Inquiries Component (Weight: 10%)
        inquiries_component = self._score_hard_inquiries(
            credit_history.hard_inquiries_last_6_months
        )
        component_scores['hard_inquiries'] = {
            'raw_value': credit_history.hard_inquiries_last_6_months,
            'normalized_score': inquiries_component,
            'weighted_score': inquiries_component * self.weights['hard_inquiries'],
            'weight': self.weights['hard_inquiries']
        }
        
        # 6. Debt-to-Income Ratio Component (Weight: 10%)
        dti_component = self._score_debt_to_income(
            credit_history.loan_emi,
            applicant.monthly_income
        )
        component_scores['debt_to_income'] = {
            'raw_value': (credit_history.loan_emi / applicant.monthly_income * 100) if applicant.monthly_income > 0 else 0,
            'normalized_score': dti_component,
            'weighted_score': dti_component * self.weights['debt_to_income'],
            'weight': self.weights['debt_to_income']
        }
        
        # 7. Job Stability Component (Weight: 5%)
        job_component = self._score_job_stability(
            employment.job_stability_months
        )
        component_scores['job_stability'] = {
            'raw_value': employment.job_stability_months,
            'normalized_score': job_component,
            'weighted_score': job_component * self.weights['job_stability'],
            'weight': self.weights['job_stability']
        }
        
        # Calculate final weighted score
        final_score = sum(
            component['weighted_score'] 
            for component in component_scores.values()
        )
        
        # Scale to 300-900 range (credit score range)
        scaled_score = int(300 + (final_score * 6))
        
        return scaled_score, component_scores
    
    def _score_cibil(self, cibil_score: int) -> float:
        """Score CIBIL component (0-100)"""
        if cibil_score >= 800:
            return 100
        elif cibil_score >= 750:
            return 90
        elif cibil_score >= 700:
            return 75
        elif cibil_score >= 650:
            return 60
        elif cibil_score >= 600:
            return 45
        else:
            return 30
    
    def _score_credit_utilization(self, utilization: float) -> float:
        """Score credit utilization (lower is better)"""
        if utilization <= 10:
            return 100
        elif utilization <= 30:
            return 85
        elif utilization <= 50:
            return 60
        elif utilization <= 70:
            return 40
        else:
            return 20
    
    def _score_payment_history(self, missed_payments: int) -> float:
        """Score payment history (fewer missed = better)"""
        if missed_payments == 0:
            return 100
        elif missed_payments == 1:
            return 70
        elif missed_payments == 2:
            return 50
        elif missed_payments <= 4:
            return 30
        else:
            return 10
    
    def _score_credit_history_length(self, months: int) -> float:
        """Score credit history length (longer is better)"""
        if months >= 60:  # 5+ years
            return 100
        elif months >= 36:  # 3+ years
            return 80
        elif months >= 24:  # 2+ years
            return 60
        elif months >= 12:  # 1+ year
            return 40
        else:
            return 20
    
    def _score_hard_inquiries(self, inquiries: int) -> float:
        """Score hard inquiries (fewer is better)"""
        if inquiries == 0:
            return 100
        elif inquiries <= 2:
            return 80
        elif inquiries <= 4:
            return 60
        elif inquiries <= 6:
            return 40
        else:
            return 20
    
    def _score_debt_to_income(self, monthly_emi: float, monthly_income: float) -> float:
        """Score debt-to-income ratio (lower is better)"""
        if monthly_income == 0:
            return 0
        
        dti = (monthly_emi / monthly_income) * 100
        
        if dti <= 20:
            return 100
        elif dti <= 35:
            return 80
        elif dti <= 50:
            return 60
        elif dti <= 65:
            return 40
        else:
            return 20
    
    def _score_job_stability(self, months: int) -> float:
        """Score job stability (longer tenure = better)"""
        if months >= 36:  # 3+ years
            return 100
        elif months >= 24:  # 2+ years
            return 80
        elif months >= 12:  # 1+ year
            return 60
        elif months >= 6:
            return 40
        else:
            return 20
    
    def determine_risk_category(self, score: int) -> str:
        """Determine risk category based on score"""
        if score >= 750:
            return "Low Risk"
        elif score >= 650:
            return "Medium Risk"
        else:
            return "High Risk"
    
    def calculate_approval_probability(self, score: int) -> float:
        """Calculate loan approval probability"""
        if score >= 800:
            return 95.0
        elif score >= 750:
            return 85.0
        elif score >= 700:
            return 70.0
        elif score >= 650:
            return 55.0
        elif score >= 600:
            return 35.0
        else:
            return 15.0
