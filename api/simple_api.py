#!/usr/bin/env python3
"""
最简单的API端点 - 不使用FastAPI，直接使用Vercel的Python函数格式
"""

import json
from datetime import datetime

def handler(request):
    """Vercel Python函数的标准handler"""
    path = request.get('path', '/')
    
    # 根据路径返回不同的响应
    if path == '/api/' or path == '/api':
        response = {
            "message": "Welcome to Micro SaaS Scout API",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "endpoints": ["/api/health", "/api/hello", "/api/stats"]
        }
    elif path == '/api/health':
        response = {
            "status": "healthy",
            "service": "micro-saas-scout-api",
            "timestamp": datetime.utcnow().isoformat()
        }
    elif path == '/api/hello':
        response = {
            "message": "Hello from Micro SaaS Scout API!",
            "timestamp": datetime.utcnow().isoformat()
        }
    elif path == '/api/stats':
        response = {
            "timestamp": datetime.utcnow().isoformat(),
            "system": "Micro SaaS Scout",
            "status": "operational"
        }
    elif path == '/api/docs':
        # 返回简单的HTML文档
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>API Documentation</title></head>
        <body>
            <h1>Micro SaaS Scout API</h1>
            <p>Simple API endpoints:</p>
            <ul>
                <li><a href="/api/">/api/</a> - Root endpoint</li>
                <li><a href="/api/health">/api/health</a> - Health check</li>
                <li><a href="/api/hello">/api/hello</a> - Hello endpoint</li>
                <li><a href="/api/stats">/api/stats</a> - System stats</li>
            </ul>
        </body>
        </html>
        """
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html
        }
    else:
        response = {
            "error": "Endpoint not found",
            "path": path,
            "timestamp": datetime.utcnow().isoformat(),
            "available_endpoints": ["/api/", "/api/health", "/api/hello", "/api/stats", "/api/docs"]
        }
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response)
        }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }