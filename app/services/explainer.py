from typing import List, Dict
from app.models.schemas import (
    CreditFactor, ImprovementAction, CreditHistory, 
    ApplicantInfo, EmploymentInfo
)

# This is the "communicator" or "financial advisor." It takes the raw math from the engine and translates it into friendly, easy-to-understand English sentences for the user to read.

class CreditExplainer:
    """
    Generates human-readable explanations for credit scores
    """
    
    def generate_factor_explanations(
        self,
        component_scores: Dict,
        applicant: ApplicantInfo,
        credit_history: CreditHistory,
        employment: EmploymentInfo
    ) -> tuple:
        """
        Generate positive, negative, and neutral factor explanations
        
        Returns:
            Tuple of (positive_factors, negative_factors, neutral_factors)
        """
        positive_factors = []
        negative_factors = []
        neutral_factors = []
        
        # Analyze each component
        for factor_name, scores in component_scores.items():
            normalized_score = scores['normalized_score']
            weight = scores['weight']
            
            # Determine impact category
            if normalized_score >= 75:
                impact = "Positive"
                factors_list = positive_factors
            elif normalized_score <= 50:
                impact = "Negative"
                factors_list = negative_factors
            else:
                impact = "Neutral"
                factors_list = neutral_factors
            
            # Generate explanation based on factor type
            explanation_data = self._explain_factor(
                factor_name, scores, applicant, credit_history, employment
            )
            
            factor = CreditFactor(
                factor=explanation_data['name'],
                current_value=explanation_data['value'],
                impact=impact,
                score_impact=explanation_data['score_impact'],
                weight=self._weight_to_text(weight),
                explanation=explanation_data['explanation']
            )
            
            factors_list.append(factor)
        
        # Sort by absolute score impact
        positive_factors.sort(key=lambda x: abs(x.score_impact), reverse=True)
        negative_factors.sort(key=lambda x: abs(x.score_impact), reverse=True)
        
        return positive_factors, negative_factors, neutral_factors
    
    def _explain_factor(
        self, 
        factor_name: str, 
        scores: Dict,
        applicant: ApplicantInfo,
        credit_history: CreditHistory,
        employment: EmploymentInfo
    ) -> Dict:
        """Generate explanation for a specific factor"""
        
        explanations = {
            'cibil_score': {
                'name': 'CIBIL Score',
                'value': str(credit_history.cibil_score),
                'score_impact': int((scores['normalized_score'] - 50) * 1.2),
                'explanation': self._explain_cibil(credit_history.cibil_score)
            },
            'credit_utilization': {
                'name': 'Credit Card Utilization',
                'value': f"{credit_history.credit_utilization}%",
                'score_impact': int((scores['normalized_score'] - 50) * 0.9),
                'explanation': self._explain_utilization(credit_history.credit_utilization)
            },
            'payment_history': {
                'name': 'Payment History',
                'value': f"{credit_history.missed_payments_last_year} missed payment(s)",
                'score_impact': int((scores['normalized_score'] - 50) * 1.5),
                'explanation': self._explain_payment_history(credit_history.missed_payments_last_year)
            },
            'credit_history_length': {
                'name': 'Credit History Length',
                'value': f"{credit_history.credit_history_length_months} months",
                'score_impact': int((scores['normalized_score'] - 50) * 0.6),
                'explanation': self._explain_history_length(credit_history.credit_history_length_months)
            },
            'hard_inquiries': {
                'name': 'Recent Credit Inquiries',
                'value': f"{credit_history.hard_inquiries_last_6_months} inquiries",
                'score_impact': int((scores['normalized_score'] - 50) * 0.8),
                'explanation': self._explain_inquiries(credit_history.hard_inquiries_last_6_months)
            },
            'debt_to_income': {
                'name': 'Debt-to-Income Ratio',
                'value': f"{(credit_history.loan_emi/applicant.monthly_income*100):.1f}%",
                'score_impact': int((scores['normalized_score'] - 50) * 0.7),
                'explanation': self._explain_dti(credit_history.loan_emi, applicant.monthly_income)
            },
            'job_stability': {
                'name': 'Employment Stability',
                'value': f"{employment.job_stability_months} months",
                'score_impact': int((scores['normalized_score'] - 50) * 0.4),
                'explanation': self._explain_job_stability(employment.job_stability_months)
            }
        }
        
        return explanations.get(factor_name, {})
    
    def _explain_cibil(self, score: int) -> str:
        """Explain CIBIL score impact"""
        if score >= 800:
            return f"Excellent credit score of {score}. This demonstrates exceptional credit management and significantly boosts your creditworthiness."
        elif score >= 750:
            return f"Very good credit score of {score}. Lenders view you as a low-risk borrower, which qualifies you for better interest rates."
        elif score >= 700:
            return f"Good credit score of {score}. You're likely to get approved, though interest rates may be slightly higher than premium offers."
        elif score >= 650:
            return f"Fair credit score of {score}. Some lenders may approve your application, but you may face higher interest rates."
        else:
            return f"Credit score of {score} needs improvement. Focus on timely payments and reducing credit utilization to boost your score."
    
    def _explain_utilization(self, utilization: float) -> str:
        """Explain credit utilization impact"""
        if utilization <= 10:
            return f"Excellent! You're using only {utilization}% of your available credit. This shows strong financial discipline."
        elif utilization <= 30:
            return f"Good credit utilization at {utilization}%. Lenders prefer to see usage below 30% of available credit."
        elif utilization <= 50:
            return f"Moderate utilization at {utilization}%. Consider reducing to below 30% to improve your score."
        else:
            return f"High utilization at {utilization}%. Using over 50% of available credit signals financial stress. Aim to bring this below 30%."
    
    def _explain_payment_history(self, missed: int) -> str:
        """Explain payment history"""
        if missed == 0:
            return "Perfect payment history! You've never missed a payment in the last year. This is the most important factor in credit scoring."
        elif missed == 1:
            return f"One missed payment in the last year. While not ideal, maintaining perfect payments going forward will help recovery."
        else:
            return f"{missed} missed payments in the last year is concerning. Consistent on-time payments are crucial for credit health."
    
    def _explain_history_length(self, months: int) -> str:
        """Explain credit history length"""
        years = months / 12
        if months >= 60:
            return f"Excellent credit history of {years:.1f} years. Longer history demonstrates sustained creditworthiness."
        elif months >= 36:
            return f"Good credit history of {years:.1f} years. This solid track record works in your favor."
        elif months >= 24:
            return f"Moderate credit history of {years:.1f} years. As your accounts age naturally, your score will improve."
        else:
            return f"Short credit history of {years:.1f} years. Build history by maintaining accounts responsibly over time."
    
    def _explain_inquiries(self, inquiries: int) -> str:
        """Explain hard inquiries"""
        if inquiries == 0:
            return "No recent credit inquiries. This shows you're not urgently seeking credit, which is viewed positively."
        elif inquiries <= 2:
            return f"{inquiries} recent credit inquiries is reasonable. Multiple inquiries in short periods can lower your score."
        else:
            return f"{inquiries} recent inquiries is high. Each inquiry can temporarily reduce your score by 5-10 points."
    
    def _explain_dti(self, emi: float, income: float) -> str:
        """Explain debt-to-income ratio"""
        dti = (emi / income * 100) if income > 0 else 0
        if dti <= 20:
            return f"Excellent DTI of {dti:.1f}%. You have significant income after debt obligations."
        elif dti <= 35:
            return f"Healthy DTI of {dti:.1f}%. Most lenders prefer DTI below 35-40%."
        elif dti <= 50:
            return f"Moderate DTI of {dti:.1f}%. Consider reducing debt or increasing income to improve borrowing capacity."
        else:
            return f"High DTI of {dti:.1f}%. Over 50% of income goes to debt, limiting ability to take additional loans."
    
    def _explain_job_stability(self, months: int) -> str:
        """Explain job stability"""
        years = months / 12
        if months >= 36:
            return f"Excellent job stability of {years:.1f} years. This demonstrates consistent income and reduces lender risk."
        elif months >= 24:
            return f"Good job tenure of {years:.1f} years shows stability."
        elif months >= 12:
            return f"Moderate job tenure of {years:.1f} years. Longer tenure would strengthen your application."
        else:
            return f"Recent job change ({years:.1f} years). Lenders prefer at least 1-2 years of job stability."
    
    def _weight_to_text(self, weight: float) -> str:
        """Convert weight to text description"""
        if weight >= 0.15:
            return "High"
        elif weight >= 0.08:
            return "Medium"
        else:
            return "Low"
    
    def generate_improvement_suggestions(
        self,
        component_scores: Dict,
        applicant: ApplicantInfo,
        credit_history: CreditHistory,
        current_score: int
    ) -> List[ImprovementAction]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Analyze each component for improvement opportunities
        for factor_name, scores in component_scores.items():
            if scores['normalized_score'] < 80:  # Room for improvement
                suggestion = self._generate_improvement_action(
                    factor_name, scores, applicant, credit_history
                )
                if suggestion:
                    suggestions.append(suggestion)
        
        # Sort by priority (high impact, easy to do first)
        suggestions.sort(
            key=lambda x: (
                {'High': 3, 'Medium': 2, 'Low': 1}[x.priority],
                {'Easy': 3, 'Medium': 2, 'Hard': 1}[x.difficulty]
            ),
            reverse=True
        )
        
        return suggestions[:5]  # Top 5 suggestions
    
    def _generate_improvement_action(
        self,
        factor_name: str,
        scores: Dict,
        applicant: ApplicantInfo,
        credit_history: CreditHistory
    ) -> ImprovementAction:
        """Generate specific improvement action"""
        
        actions = {
            'credit_utilization': ImprovementAction(
                action=f"Reduce credit card utilization from {credit_history.credit_utilization}% to below 30%",
                expected_impact=int((80 - scores['normalized_score']) * scores['weight'] * 6),
                timeline="1-2 months",
                difficulty="Medium",
                priority="High"
            ) if credit_history.credit_utilization > 30 else None,
            
            'payment_history': ImprovementAction(
                action="Maintain 100% on-time payments for next 12 months",
                expected_impact=int((90 - scores['normalized_score']) * scores['weight'] * 6),
                timeline="12 months",
                difficulty="Easy",
                priority="High"
            ) if credit_history.missed_payments_last_year > 0 else None,
            
            'hard_inquiries': ImprovementAction(
                action="Avoid new credit applications for 6 months",
                expected_impact=int((80 - scores['normalized_score']) * scores['weight'] * 6),
                timeline="6 months",
                difficulty="Easy",
                priority="Medium"
            ) if credit_history.hard_inquiries_last_6_months > 3 else None,
            
            'debt_to_income': ImprovementAction(
                action=f"Pay down existing loans to reduce monthly EMI by ₹{credit_history.loan_emi * 0.2:.0f}",
                expected_impact=int((75 - scores['normalized_score']) * scores['weight'] * 6),
                timeline="6-12 months",
                difficulty="Hard",
                priority="Medium"
            ) if (credit_history.loan_emi / applicant.monthly_income * 100) > 35 else None,
        }
        
        return actions.get(factor_name)
