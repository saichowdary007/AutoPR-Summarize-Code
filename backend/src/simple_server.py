"""
Simple HTTP server to test if the backend works.
This file creates a minimal FastAPI application to check if it can run.
"""

import os
import uvicorn
import logging
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("simple_server")

# Create a minimal FastAPI app
app = FastAPI(title="Simple Test Server")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting Simple Test Server on {host}:{port}")
    
    # Run the application
    uvicorn.run(
        "simple_server:app",
        host=host,
        port=port,
        reload=False
    ) 