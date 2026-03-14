# CreditExplain AI - Explainable Credit Risk Assessment API

## Overview
An intelligent FastAPI that provides credit risk assessments with detailed explanations using explainable AI principles. Built to demonstrate explainable AI in the fintech and banking industry.

```
📦 
├─ .env
├─ .gitignore
├─ README.md
├─ app
│  ├─ __init__.py
│  ├─ __pycache__
│  │  ├─ __init__.cpython-313.pyc
│  │  └─ main.cpython-313.pyc
│  ├─ main.py
│  ├─ models
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  └─ schemas.cpython-313.pyc
│  │  └─ schemas.py
│  ├─ routers
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  └─ credit.cpython-313.pyc
│  │  └─ credit.py
│  ├─ services
│  │  ├─ __init__.py
│  │  ├─ __pycache__
│  │  │  ├─ __init__.cpython-313.pyc
│  │  │  ├─ credit_engine.cpython-313.pyc
│  │  │  └─ explainer.cpython-313.pyc
│  │  ├─ credit_engine.py
│  │  └─ explainer.py
│  └─ utils
│     ├─ __init__.py
│     └─ helpers.py
└─ requirements.txt
```

## Features
- 🎯 Comprehensive credit scoring with 7 key factors
- 🧠 Explainable AI - understand why scores are what they are
- 📊 Factor-by-factor breakdown with impact analysis
- 💡 Actionable improvement suggestions
- 🛣️ Month-by-month credit improvement roadmaps
- 📝 Automated API documentation

## Tech Stack
- **Framework**: FastAPI
- **ML**: scikit-learn, pandas, numpy
- **Validation**: Pydantic
- **Documentation**: Swagger/OpenAPI

## Installation
```bash
# Clone repository
git clone <your-repo-url>
cd MLOps_Lab3_FastAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API
```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## API Endpoints

### POST /api/v1/credit/assess
Comprehensive credit assessment with explanations

### GET /api/v1/credit/improvement-roadmap
Generate credit score improvement plan

## Example Request
```json
{
  "applicant": {
    "name": "Siddharth Mohapatra",
    "pan": "ABCDE1234F",
    "phone": "+919861364100",
    "email": "siddharth.m33@email.com",
    "age": 25,
    "monthly_income": 50000
  },
  "credit_history": {
    "cibil_score": 720,
    "credit_cards": 3,
    "total_credit_limit": 500000,
    "credit_utilization": 35,
    "active_loans": 2,
    "total_loan_amount": 1000000,
    "loan_emi": 25000,
    "credit_history_length_months": 48,
    "missed_payments_last_year": 0,
    "hard_inquiries_last_6_months": 2
  },
  "employment": {
    "employment_type": "Salaried",
    "job_stability_months": 36,
    "employer_type": "Private Sector"
  },
  "requested_loan_amount": 500000,
  "loan_purpose": "Personal Loan"
}
```

## Example Response
```json
{
  "request_id": "e552cb9c-9221-4696-8bca-1248f1732180",
  "timestamp": "2026-03-13T21:28:22.303364",
  "applicant_name": "Amit Kumar",
  "final_score": 771,
  "explanation": {
    "score": 771,
    "risk_category": "Low Risk",
    "approval_probability": 85,
    "top_positive_factors": [
      {
        "factor": "Payment History",
        "current_value": "0 missed payment(s)",
        "impact": "Positive",
        "score_impact": 75,
        "weight": "High",
        "explanation": "Perfect payment history! You've never missed a payment in the last year. This is the most important factor in credit scoring."
      },
      {
        "factor": "CIBIL Score",
        "current_value": "720",
        "impact": "Positive",
        "score_impact": 30,
        "weight": "High",
        "explanation": "Good credit score of 720. You're likely to get approved, though interest rates may be slightly higher than premium offers."
      },
      {
        "factor": "Recent Credit Inquiries",
        "current_value": "2 inquiries",
        "impact": "Positive",
        "score_impact": 24,
        "weight": "Medium",
        "explanation": "2 recent credit inquiries is reasonable. Multiple inquiries in short periods can lower your score."
      }
    ],
    "top_negative_factors": [],
    "neutral_factors": [
      {
        "factor": "Credit Card Utilization",
        "current_value": "35.0%",
        "impact": "Neutral",
        "score_impact": 9,
        "weight": "High",
        "explanation": "Moderate utilization at 35.0%. Consider reducing to below 30% to improve your score."
      },
      {
        "factor": "Debt-to-Income Ratio",
        "current_value": "50.0%",
        "impact": "Neutral",
        "score_impact": 7,
        "weight": "Medium",
        "explanation": "Moderate DTI of 50.0%. Consider reducing debt or increasing income to improve borrowing capacity."
      }
    ],
    "improvement_suggestions": [
      {
        "action": "Reduce credit card utilization from 35.0% to below 30%",
        "expected_impact": 18,
        "timeline": "1-2 months",
        "difficulty": "Medium",
        "priority": "High"
      },
      {
        "action": "Pay down existing loans to reduce monthly EMI by ₹5000",
        "expected_impact": 9,
        "timeline": "6-12 months",
        "difficulty": "Hard",
        "priority": "Medium"
      }
    ],
    "score_breakdown": {
      "cibil_score": 22.5,
      "credit_utilization": 9,
      "payment_history": 20,
      "credit_history_length": 8,
      "hard_inquiries": 8,
      "debt_to_income": 6,
      "job_stability": 5
    }
  },
  "lending_decision": "Approve",
  "recommended_loan_amount": 500000,
  "recommended_interest_rate": 10.5,
  "conditions": [
    "Standard terms apply",
    "Pre-approved for premium rate"
  ]
}
Response headers
 access-control-allow-credentials: true 
 access-control-allow-origin: http://localhost:8000 
 content-length: 2157 
 content-type: application/json 
 date: Sat,14 Mar 2026 01:28:21 GMT 
 server: uvicorn 
 vary: Origin
```

## Author
Siddharth Mohapatra

Northeastern University - IE 7374 MLOps Lab 3


