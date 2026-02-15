from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import logging
from datetime import datetime
from typing import Dict

from backend.database.database import get_db
from backend.utils.data_pipeline import DataPipeline
from backend.database.models import Source

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/crawl", tags=["crawl"])

# 全局数据管道实例
pipeline = DataPipeline()

class CrawlRequest(BaseModel):
    platform: str = "hackernews"
    max_posts: int = 30
    force: bool = False

class CrawlResponse(BaseModel):
    status: str
    message: str
    crawl_id: str
    started_at: datetime
    estimated_duration: int
    platform: str

class CrawlStatus(BaseModel):
    crawl_id: str
    status: str
    platform: str
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    stats: Optional[Dict]
    error: Optional[str]

# 存储正在进行的爬取任务
active_crawls: Dict[str, Dict] = {}

@router.post("/start", response_model=CrawlResponse)
async def start_crawl(
    request: CrawlRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """启动数据爬取任务"""
    try:
        # 检查数据源是否活跃
        source = db.query(Source).filter(
            Source.platform == request.platform,
            Source.is_active == True
        ).first()
        
        if not source and not request.force:
            raise HTTPException(
                status_code=400,
                detail=f"Source {request.platform} is not active or not configured"
            )
        
        # 生成爬取ID
        import uuid
        crawl_id = str(uuid.uuid4())[:8]
        
        # 记录爬取任务
        active_crawls[crawl_id] = {
            "id": crawl_id,
            "platform": request.platform,
            "status": "running",
            "started_at": datetime.utcnow(),
            "request": request.dict()
        }
        
        # 在后台运行爬取任务
        background_tasks.add_task(
            run_crawl_task,
            crawl_id=crawl_id,
            platform=request.platform,
            max_posts=request.max_posts
        )
        
        logger.info(f"Started crawl {crawl_id} for platform {request.platform}")
        
        return CrawlResponse(
            status="started",
            message=f"Crawl started for {request.platform}",
            crawl_id=crawl_id,
            started_at=active_crawls[crawl_id]["started_at"],
            estimated_duration=60,  # 估计60秒
            platform=request.platform
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting crawl: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/status/{crawl_id}", response_model=CrawlStatus)
async def get_crawl_status(crawl_id: str):
    """获取爬取任务状态"""
    try:
        if crawl_id not in active_crawls:
            raise HTTPException(status_code=404, detail="Crawl not found")
        
        crawl_info = active_crawls[crawl_id]
        
        response = CrawlStatus(
            crawl_id=crawl_id,
            status=crawl_info["status"],
            platform=crawl_info["platform"],
            started_at=crawl_info["started_at"],
            completed_at=crawl_info.get("completed_at"),
            duration_seconds=crawl_info.get("duration_seconds"),
            stats=crawl_info.get("stats"),
            error=crawl_info.get("error")
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting crawl status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/active")
async def get_active_crawls():
    """获取所有活跃的爬取任务"""
    try:
        active = []
        for crawl_id, crawl_info in active_crawls.items():
            if crawl_info["status"] == "running":
                active.append({
                    "crawl_id": crawl_id,
                    "platform": crawl_info["platform"],
                    "started_at": crawl_info["started_at"],
                    "duration": (datetime.utcnow() - crawl_info["started_at"]).total_seconds()
                })
        
        return {
            "active_crawls": active,
            "total_active": len(active)
        }
        
    except Exception as e:
        logger.error(f"Error getting active crawls: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{crawl_id}/cancel")
async def cancel_crawl(crawl_id: str):
    """取消爬取任务"""
    try:
        if crawl_id not in active_crawls:
            raise HTTPException(status_code=404, detail="Crawl not found")
        
        if active_crawls[crawl_id]["status"] != "running":
            raise HTTPException(status_code=400, detail="Crawl is not running")
        
        # 标记为取消（实际实现需要中断任务）
        active_crawls[crawl_id]["status"] = "cancelled"
        active_crawls[crawl_id]["completed_at"] = datetime.utcnow()
        
        logger.info(f"Cancelled crawl {crawl_id}")
        
        return {
            "status": "cancelled",
            "message": f"Crawl {crawl_id} has been cancelled",
            "crawl_id": crawl_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling crawl: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/sources")
async def get_crawl_sources(db: Session = Depends(get_db)):
    """获取可用的数据源"""
    try:
        sources = db.query(Source).all()
        
        source_list = []
        for source in sources:
            source_list.append({
                "id": source.id,
                "name": source.name,
                "platform": source.platform,
                "is_active": source.is_active,
                "last_crawled_at": source.last_crawled_at,
                "total_demands_found": source.total_demands_found,
                "success_rate": source.success_rate,
                "crawl_interval_hours": source.crawl_interval_hours
            })
        
        return {
            "sources": source_list,
            "total_sources": len(source_list)
        }
        
    except Exception as e:
        logger.error(f"Error getting crawl sources: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stats")
async def get_crawl_stats():
    """获取爬取统计信息"""
    try:
        pipeline_stats = pipeline.get_pipeline_stats()
        
        # 计算总体统计
        total_crawls = len(active_crawls)
        completed_crawls = sum(1 for c in active_crawls.values() if c["status"] in ["completed", "failed", "cancelled"])
        running_crawls = total_crawls - completed_crawls
        
        return {
            "pipeline_stats": pipeline_stats,
            "crawl_jobs": {
                "total": total_crawls,
                "running": running_crawls,
                "completed": completed_crawls,
                "failed": sum(1 for c in active_crawls.values() if c["status"] == "failed")
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting crawl stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def run_crawl_task(crawl_id: str, platform: str, max_posts: int):
    """后台运行爬取任务"""
    try:
        logger.info(f"Running crawl task {crawl_id} for {platform}")
        
        start_time = datetime.utcnow()
        
        # 根据平台选择爬虫
        if platform == "hackernews":
            result = pipeline.run_hackernews_pipeline(max_posts=max_posts)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
        
        # 更新任务状态
        active_crawls[crawl_id]["status"] = "completed" if result["status"] == "success" else "failed"
        active_crawls[crawl_id]["completed_at"] = datetime.utcnow()
        active_crawls[crawl_id]["duration_seconds"] = (active_crawls[crawl_id]["completed_at"] - start_time).total_seconds()
        active_crawls[crawl_id]["stats"] = result.get("stats", {})
        
        if result["status"] == "error":
            active_crawls[crawl_id]["error"] = result.get("error", "Unknown error")
        
        logger.info(f"Crawl task {crawl_id} completed with status: {active_crawls[crawl_id]['status']}")
        
    except Exception as e:
        logger.error(f"Crawl task {crawl_id} failed: {str(e)}")
        
        active_crawls[crawl_id]["status"] = "failed"
        active_crawls[crawl_id]["completed_at"] = datetime.utcnow()
        active_crawls[crawl_id]["error"] = str(e)
        
        if "started_at" in active_crawls[crawl_id]:
            active_crawls[crawl_id]["duration_seconds"] = (
                active_crawls[crawl_id]["completed_at"] - active_crawls[crawl_id]["started_at"]
            ).total_seconds()

# 修复：添加缺少的导入
from pydantic import BaseModel
from typing import Optional