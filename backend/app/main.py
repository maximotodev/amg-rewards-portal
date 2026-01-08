import time
import uuid
import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.routes import receipts
from app.core.config import settings
from app.core.db import engine, Base, get_db

# 1. Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("amg-portal")

# 2. Instantiate App 
app = FastAPI(title=settings.APP_NAME)

# 3. DB Table Creation (Automatic migration check for demo safety)
Base.metadata.create_all(bind=engine)

# 4. Middleware: Structured Logging & Request ID
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(f"RID={request_id} METHOD={request.method} PATH={request.url.path} STATUS={response.status_code} LATENCY={process_time:.2f}ms")
    
    response.headers["X-Request-ID"] = request_id
    return response

# 5. Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Routes
app.include_router(receipts.router)

@app.get("/health", tags=["system"])
def health_check(db: Session = Depends(get_db)):
    """
    Deep Health Check: Verifies API and Database connectivity.
    Essential for AWS ALB Target Group monitoring.
    """
    try:
        # Verify database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Database connection unreachable")

@app.get("/")
def root():
    return {"message": "AMG Rewards API is online"}
