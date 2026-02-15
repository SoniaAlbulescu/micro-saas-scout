from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from datetime import datetime

# 导入路由
from api.demands.route import router as demands_router
from api.crawl.route import router as crawl_router
from backend.database.database import init_db, db

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="Micro SaaS Scout API",
    description="出海工具需求挖掘系统后端API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(demands_router)
app.include_router(crawl_router)

# 健康检查端点
@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    try:
        # 测试数据库连接
        db.test_connection()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "micro-saas-scout-api",
            "version": "1.0.0",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/api/")
async def root():
    """API根端点"""
    return {
        "message": "Welcome to Micro SaaS Scout API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "endpoints": {
            "demands": "/api/demands",
            "health": "/api/health",
            "stats": "/api/demands/stats/summary"
        }
    }

@app.get("/api/stats")
async def system_stats():
    """系统统计信息"""
    try:
        # 获取数据库统计
        db_stats = db.get_stats()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": "Micro SaaS Scout",
            "database": db_stats,
            "environment": os.getenv("ENVIRONMENT", "development"),
            "api_version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Error getting system stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("Starting Micro SaaS Scout API...")
    
    try:
        # 初始化数据库
        if init_db():
            logger.info("✅ Database initialized successfully")
        else:
            logger.error("❌ Database initialization failed")
            
        # 打印环境信息
        env = os.getenv("ENVIRONMENT", "development")
        logger.info(f"Running in {env} environment")
        
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("Shutting down Micro SaaS Scout API...")

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
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # 开发服务器配置
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )