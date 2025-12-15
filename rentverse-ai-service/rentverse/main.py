"""
Main FastAPI application for RentVerse AI Service.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from rentverse.auth import router as auth_router
from .api.routes import health, prediction, classification
from .api.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware
from .models.ml_models import get_model
from .core.exceptions import ModelNotFoundError
from .config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    logger.info("Starting RentVerse AI Service...")
    try:
        # model = get_model()
        logger.info(f"Model loaded successfully")
        # logger.info(f"Model loaded successfully: {model.model_version}")

    except ModelNotFoundError as e:
        logger.error(f"Failed to load model on startup: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during startup: {e}")
    logger.info("RentVerse AI Service started successfully")
    yield
<<<<<<< Updated upstream:rentverse-ai-service/rentverse/main.py

    # Shutdown
=======
>>>>>>> Stashed changes:rentverse-ai-service-main/rentverse/main.py
    logger.info("Shutting down RentVerse AI Service...")


# Create FastAPI application
app = FastAPI(
    title="RentVerse AI Service",
    description="AI-powered rent price prediction service for real estate properties",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Add custom middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

# ----------------------------
# Include routers (correctly)
# ----------------------------
app.include_router(auth_router)  # Auth router
app.include_router(health.router, prefix="/api/v1")  # Health
app.include_router(prediction.router, prefix="/api/v1")  # Prediction
app.include_router(classification.router, prefix="/api/v1")  # Classification

# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "RentVerse AI Service",
        "version": "1.0.0",
        "description": "AI-powered rent price prediction service",
        "docs": "/docs",
        "health": "/api/v1/health",
        "predict": "/api/v1/predict",
        "classify": "/api/v1/classify",
        "auth": "/auth",
        "endpoints": {
            "price_prediction": "/api/v1/classify/price",
            "listing_approval": "/api/v1/classify/approval",
            "single_prediction": "/api/v1/predict/single",
            "batch_prediction": "/api/v1/predict/batch",
            "auth_login": "/auth/login",
            "auth_verify_otp": "/auth/verify-otp"
        }
    }

@app.options("/{path:path}")
async def options_handler(path: str):
    return {"message": "OK"}

# ----------------------------
# Exception handlers
# ----------------------------
@app.exception_handler(ModelNotFoundError)
async def model_not_found_handler(request, exc):
    logger.error(f"Model not found: {exc.message}")
    return JSONResponse(
        status_code=503,
        content={"error": "Model not available", "detail": exc.message, "code": 503, "status": "error"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred", "code": 500, "status": "error"}
    )

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "rentverse.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )

    # trigger workflow

