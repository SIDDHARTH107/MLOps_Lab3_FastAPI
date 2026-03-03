from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import credit

# This file is the starting point of my entire application. It's the file that runs when we start the server. We can think of it as the building that houses the front desk (our credit.py router) and all the workers (our engine and explainer).

# Creating FastAPI app
app = FastAPI(
    title="CreditExplain AI",
    description="Explainable Credit Risk Assessment API - Understanding credit decisions through AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Including routers
app.include_router(credit.router)

# Health checking endpoint
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "CreditExplain AI API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

#  This is the foundation of the house. It sets up the server, turns off strict security blockers so other apps can talk to it, plugs in our specific credit features, and sets up a quick "pulse check" so we know the server is alive.
