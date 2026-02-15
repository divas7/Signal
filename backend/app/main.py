from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="NIFTY50 Options Signal Console API",
    version="0.1.0",
    description="Backend for NIFTY50 Options Signal Console"
)

# CORS Configuration
# In production, this should be restricted to the specific frontend domain
origins = [
    "*" # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.endpoints import setup, signals

app.include_router(setup.router, prefix="/api/v1/setup", tags=["setup"])
app.include_router(signals.router, prefix="/api/v1/signals", tags=["signals"])

@app.on_event("startup")
async def startup_event():
    # In a real app, initialize DB connection pool here
    pass

@app.get("/")
def read_root():
    return {"message": "NIFTY50 Options Signal Console API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
