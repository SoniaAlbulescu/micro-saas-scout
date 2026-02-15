from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 检查环境变量
        db_url_set = "DATABASE_URL" in os.environ
        
        response = {
            "status": "healthy",
            "service": "micro-saas-scout-api",
            "timestamp": datetime.utcnow().isoformat(),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "database_configured": db_url_set,
            "endpoints": {
                "hello": "/api/hello",
                "demands": "/api/demands",
                "stats": "/api/stats",
                "docs": "/api/docs"
            }
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
        return