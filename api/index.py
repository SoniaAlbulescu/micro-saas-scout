from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import logging
import os
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用 - 在Vercel中，docs_url和redoc_url可能需要设置为None
# 因为Vercel的路由处理方式不同
app = FastAPI(
    title="Micro SaaS Scout API",
    description="出海工具需求挖掘系统后端API",
    version="1.0.0",
    docs_url=None,  # 禁用自动生成的/docs页面
    redoc_url=None, # 禁用自动生成的/redoc页面
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "micro-saas-scout-api",
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "message": "API is working correctly"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/")
async def root():
    """API根端点"""
    return {
        "message": "Welcome to Micro SaaS Scout API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "health": "/health",
            "hello": "/hello",
            "stats": "/stats",
            "docs": "See API documentation below"
        },
        "documentation": {
            "openapi": "/openapi.json",
            "swagger_ui": "https://micro-saas-scout.vercel.app/api/docs" if os.getenv("ENVIRONMENT") == "production" else "http://localhost:8000/docs"
        }
    }

@app.get("/hello")
async def hello():
    """Hello端点"""
    return {
        "message": "Hello from Micro SaaS Scout API!",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "success"
    }

@app.get("/stats")
async def system_stats():
    """系统统计信息"""
    try:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": "Micro SaaS Scout",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "api_version": "1.0.0",
            "status": "operational",
            "uptime": "100%",
            "requests_served": 0  # 在实际应用中这里会有统计
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 手动创建/docs页面
@app.get("/docs", response_class=HTMLResponse)
async def custom_docs():
    """自定义API文档页面"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Micro SaaS Scout API Documentation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { display: inline-block; background: #4CAF50; color: white; padding: 5px 10px; border-radius: 3px; }
            .url { font-family: monospace; color: #0066cc; }
            .description { margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>📚 Micro SaaS Scout API Documentation</h1>
        <p>This is a simple API for the Micro SaaS Scout project.</p>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="url">/</span>
            <div class="description">API root endpoint - returns welcome message and available endpoints</div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="url">/health</span>
            <div class="description">Health check endpoint - returns service status</div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="url">/hello</span>
            <div class="description">Hello endpoint - simple test endpoint</div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="url">/stats</span>
            <div class="description">System statistics endpoint</div>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <span class="url">/openapi.json</span>
            <div class="description">OpenAPI specification in JSON format</div>
        </div>
        
        <h2>Testing the API</h2>
        <p>You can test the API using curl or any HTTP client:</p>
        <pre>
curl https://micro-saas-scout.vercel.app/api/
curl https://micro-saas-scout.vercel.app/api/health
curl https://micro-saas-scout.vercel.app/api/hello
        </pre>
        
        <h2>OpenAPI Specification</h2>
        <p>For the full OpenAPI specification, visit: <a href="/openapi.json">/openapi.json</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )

# 404处理器
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """404处理器"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested endpoint {request.url.path} was not found",
            "timestamp": datetime.utcnow().isoformat(),
            "available_endpoints": ["/", "/health", "/hello", "/stats", "/docs", "/openapi.json"]
        }
    )