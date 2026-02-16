#!/usr/bin/env python3
"""
简单的API测试 - 不需要安装FastAPI
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
import os

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理GET请求"""
        # 设置响应头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 根据路径返回不同的响应
        if self.path == '/':
            response = {
                "message": "Welcome to Micro SaaS Scout API",
                "version": "1.0.0",
                "timestamp": datetime.utcnow().isoformat(),
                "endpoints": {
                    "health": "/health",
                    "hello": "/hello",
                    "stats": "/stats"
                }
            }
        elif self.path == '/health':
            response = {
                "status": "healthy",
                "service": "micro-saas-scout-api",
                "timestamp": datetime.utcnow().isoformat(),
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        elif self.path == '/hello':
            response = {
                "message": "Hello from Micro SaaS Scout API!",
                "timestamp": datetime.utcnow().isoformat()
            }
        elif self.path == '/stats':
            response = {
                "timestamp": datetime.utcnow().isoformat(),
                "system": "Micro SaaS Scout",
                "status": "operational",
                "api_version": "1.0.0"
            }
        else:
            response = {
                "error": "Endpoint not found",
                "path": self.path,
                "timestamp": datetime.utcnow().isoformat(),
                "available_endpoints": ["/", "/health", "/hello", "/stats"]
            }
        
        # 发送响应
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=8000):
    """启动HTTP服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print(f"🚀 服务器启动在 http://localhost:{port}")
    print(f"📡 可用端点:")
    print(f"  • http://localhost:{port}/")
    print(f"  • http://localhost:{port}/health")
    print(f"  • http://localhost:{port}/hello")
    print(f"  • http://localhost:{port}/stats")
    print("\n按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务器停止")
        httpd.server_close()

if __name__ == '__main__':
    run_server()