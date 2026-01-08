from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import receipts
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(receipts.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
