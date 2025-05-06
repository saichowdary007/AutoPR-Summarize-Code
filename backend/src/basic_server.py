"""
Very basic HTTP server using Python's built-in http.server module.
This is a fallback to test if we can run a server without FastAPI.
"""

import os
import logging
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("basic_server")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Default headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Simple routing
        if self.path == "/" or self.path == "/api":
            hostname = socket.gethostname()
            response = {
                "message": "Hello from the Basic Python HTTP Server!",
                "status": "Running",
                "host": hostname,
                "path": self.path,
            }
        elif self.path == "/health":
            response = {"status": "OK", "server": "Basic Python HTTP Server"}
        else:
            response = {"error": "Not found", "path": self.path}

        # Send response
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        # Override to use our logger
        logger.info(
            "%s - - [%s] %s"
            % (self.address_string(), self.log_date_time_string(), format % args)
        )


if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))

    # Create and start the server
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    logger.info(f"Starting Basic HTTP Server on http://{host}:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    finally:
        httpd.server_close()
        logger.info("Server closed")
