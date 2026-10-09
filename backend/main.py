"""
Main entry point for the File Comparison Backend
"""

import uvicorn
from app.main import app
from app.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level=settings.log_level.lower(),
        workers=1
    )