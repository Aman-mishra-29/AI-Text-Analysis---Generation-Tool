import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

# Import routers
from app.routes import summarize, plagiarism, autocorrect

from app.config import settings
from app.api import history

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# ---------------------------------------------------
# Logging Configuration (Production Level)
# ---------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("main")

# ---------------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------------
app = FastAPI(
    title="Text AI Tool API",
    description="Summarization, Plagiarism Detection & Autocorrect API",
    version="1.0.0"
)

# ---------------------------------------------------
# Middleware (CORS)
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Request Logging Middleware
# ---------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal Server Error"}
        )

    process_time = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"Completed {request.method} {request.url} "
        f"Status: {response.status_code} "
        f"Time: {process_time}ms"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response

# ---------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Global Exception: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Something went wrong",
            "details": str(exc)
        }
    )

# ---------------------------------------------------
# Health Check Route
# ---------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "message": "API is running successfully"
    }

# ---------------------------------------------------
# Root Route
# ---------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Text AI Tool API 🚀",
        "features": [
            "Text Summarization",
            "Plagiarism Detection",
            "Autocorrect"
        ]
    }

# ---------------------------------------------------
# Include Routers
# ---------------------------------------------------
app.include_router(summarize.router, prefix="/api/v1/summarize", tags=["Summarization"])
app.include_router(plagiarism.router, prefix="/api/v1/plagiarism", tags=["Plagiarism"])
app.include_router(autocorrect.router, prefix="/api/v1/autocorrect", tags=["Autocorrect"])
app.include_router(history.router)

# ---------------------------------------------------
# Startup Event
# ---------------------------------------------------
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Text AI Tool API...")
    # Load models here if needed (future optimization)
    # Example:
    # summarizer_model.load()

# ---------------------------------------------------
# Shutdown Event
# ---------------------------------------------------
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Shutting down Text AI Tool API...")