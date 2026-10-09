"""
FastAPI application factory
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
import logging
import time
import os
from datetime import datetime

from .config import get_settings, create_directories
from .dependencies import log_requests
from .models import APIError, HealthResponse

# Initialize settings
settings = get_settings()

# Create necessary directories
create_directories()

# Configure enhanced logging
from utils.logger import setup_logging
setup_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    global start_time
    start_time = time.time()

    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Upload directory: {settings.upload_dir}")
    logger.info(f"Max file size: {settings.max_file_size_mb}MB")

    # Create storage directories
    for directory in [settings.upload_dir, settings.processed_dir, settings.export_dir]:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Storage directory ready: {directory}")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")
    # Cleanup temporary files if needed
    logger.info("Application shutdown complete")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend API for file comparison system",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan
    )

    # Add middleware
    setup_middleware(app)

    # Add exception handlers
    setup_exception_handlers(app)

    # Include routers
    setup_routes(app)

    # Startup and shutdown events
    setup_events(app)

    return app


def setup_middleware(app: FastAPI) -> None:
    """Setup application middleware"""

    # Compression middleware
    if settings.enable_compression:
        app.add_middleware(GZipMiddleware, minimum_size=1000)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request logging middleware
    app.middleware("http")(log_requests)


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers"""

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An internal server error occurred",
                    "details": str(exc) if settings.debug else None
                },
                "timestamp": datetime.now().isoformat(),
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        """Handle 404 errors"""
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": "The requested resource was not found",
                    "details": {"path": str(request.url.path)}
                },
                "timestamp": datetime.now().isoformat(),
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(413)
    async def payload_too_large_handler(request: Request, exc):
        """Handle 413 errors"""
        return JSONResponse(
            status_code=413,
            content={
                "success": False,
                "error": {
                    "code": "PAYLOAD_TOO_LARGE",
                    "message": f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
                },
                "timestamp": datetime.now().isoformat(),
                "request_id": getattr(request.state, "request_id", None)
            }
        )


def setup_routes(app: FastAPI) -> None:
    """Setup application routes"""

    # Import API routers
    try:
        import sys
        import os

        # Add the backend directory to sys.path
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)

        from api.routes.files import router as files_router
        from api.routes.comparison import router as comparison_router
        from api.routes.extraction import router as extraction_router

        # Include API routers
        app.include_router(files_router, prefix="/api/files", tags=["Files"])
        app.include_router(comparison_router, prefix="/api/comparison", tags=["Comparison"])
        app.include_router(extraction_router, prefix="/api/extraction", tags=["Extraction"])

        logger.info("API routes loaded successfully")

    except ImportError as e:
        logger.warning(f"Could not import API routes: {e}")
        logger.info("Running with minimal routes (health check only)")

    # Health check endpoint
    @app.get("/api/health", response_model=HealthResponse, tags=["Health"])
    async def health_check():
        """Enhanced health check endpoint"""
        import psutil
        import asyncio
        
        try:
            # Get system metrics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Check storage directories
            storage_status = {}
            for name, path in [
                ("uploads", settings.upload_dir),
                ("processed", settings.processed_dir), 
                ("exports", settings.export_dir)
            ]:
                try:
                    if os.path.exists(path):
                        stat = os.statvfs(path)
                        free_space = stat.f_bavail * stat.f_frsize
                        total_space = stat.f_blocks * stat.f_frsize
                        storage_status[name] = {
                            "status": "available",
                            "free_space_gb": round(free_space / (1024**3), 2),
                            "total_space_gb": round(total_space / (1024**3), 2),
                            "usage_percent": round((1 - free_space/total_space) * 100, 2)
                        }
                    else:
                        storage_status[name] = {"status": "missing", "path": path}
                except Exception as e:
                    storage_status[name] = {"status": "error", "error": str(e)}
            
            # Test processor availability
            processor_status = {}
            try:
                from processors.csv_processor import CSVProcessor
                processor_status["csv"] = "available"
            except ImportError:
                processor_status["csv"] = "unavailable"
            
            try:
                from processors.excel_processor import ExcelProcessor
                processor_status["excel"] = "available"
            except ImportError:
                processor_status["excel"] = "unavailable"
                
            try:
                from processors.pdf_processor import PDFProcessor
                processor_status["pdf"] = "available"
            except ImportError:
                processor_status["pdf"] = "unavailable"

            return HealthResponse(
                status="healthy",
                timestamp=datetime.now(),
                version=settings.app_version,
                uptime=int(time.time() - start_time),
                system_info={
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory.percent,
                    "disk_usage": disk.percent
                },
                dependencies={
                    "file_storage": "available",
                    "processors": "ready",
                    "compression_enabled": str(settings.enable_compression),
                    "cache_enabled": str(settings.cache_enabled)
                }
            )
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return HealthResponse(
                status="unhealthy",
                timestamp=datetime.now(),
                version=settings.app_version,
                uptime=int(time.time() - start_time),
                system_info={"error_message": str(e), "cpu_usage": 0.0, "memory_usage": 0.0, "disk_usage": 0.0},
                dependencies={"status": "health_check_failed"}
            )

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs_url": "/docs" if settings.debug else None,
            "health_url": "/api/health"
        }


def setup_events(app: FastAPI) -> None:
    """Setup application startup and shutdown events"""
    pass


# Global start time for uptime calculation
start_time = time.time()

# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        workers=1 if settings.debug else settings.workers
    )