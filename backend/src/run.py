import os
import uvicorn
import logging
import sys
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("pr_assistant")

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "True").lower() in ["true", "1", "yes"]
    
    logger.info(f"Starting PR Summary & Code Review Assistant API on {host}:{port}")
    
    try:
        # Run the application with uvicorn
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload
        )
    except Exception as e:
        logger.error(f"Error running server with uvicorn: {e}")
        
        # Fallback to importing the app directly and running with a simple HTTP server
        logger.info("Trying alternative method...")
        try:
            from main import app
            import uvicorn.main
            
            # Create a new Config instance manually
            config = uvicorn.Config(app, host=host, port=port)
            server = uvicorn.Server(config)
            server.run()
        except Exception as e2:
            logger.error(f"Alternative method also failed: {e2}")
            sys.exit(1) 