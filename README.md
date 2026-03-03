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
cd credit-explain-api

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

## Author
Siddharth Mohapatra

Northeastern University - IE 7374 MLOps Lab 3


