from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from backend.database.database import get_db
from backend.database.models import Demand
from pydantic import BaseModel

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/demands", tags=["demands"])

# Pydantic模型
class DemandCreate(BaseModel):
    title: str
    description: str
    problem: str
    user_role: Optional[str] = None
    company_size: Optional[str] = None
    tech_level: Optional[str] = None
    budget_range: Optional[str] = None
    scenario: Optional[str] = None
    pain_points: Optional[List[str]] = None
    existing_solutions: Optional[List[str]] = None
    pricing_signals: Optional[List[str]] = None
    search_volume: Optional[int] = 0
    competitor_users: Optional[int] = 0
    growth_rate: Optional[float] = 0.0
    technical_complexity: Optional[str] = "medium"
    dev_time_weeks: Optional[int] = 4
    main_tech_stack: Optional[List[str]] = None
    demand_strength_score: Optional[float] = 0.0
    market_size_score: Optional[float] = 0.0
    willingness_to_pay_score: Optional[float] = 0.0
    technical_feasibility_score: Optional[float] = 0.0
    passive_income_fit_score: Optional[float] = 0.0
    overall_score: Optional[float] = 0.0
    recommended_pricing: Optional[str] = None
    mvp_features: Optional[List[str]] = None
    source_platform: Optional[str] = None
    source_url: Optional[str] = None
    tags: Optional[List[str]] = None
    tool_type: Optional[str] = None

class DemandResponse(BaseModel):
    id: str
    title: str
    description: str
    problem: str
    user_role: Optional[str]
    company_size: Optional[str]
    tech_level: Optional[str]
    budget_range: Optional[str]
    scenario: Optional[str]
    pain_points: Optional[List[str]]
    existing_solutions: Optional[List[str]]
    pricing_signals: Optional[List[str]]
    search_volume: int
    competitor_users: int
    growth_rate: float
    technical_complexity: str
    dev_time_weeks: int
    main_tech_stack: Optional[List[str]]
    demand_strength_score: float
    market_size_score: float
    willingness_to_pay_score: float
    technical_feasibility_score: float
    passive_income_fit_score: float
    overall_score: float
    recommended_pricing: Optional[str]
    mvp_features: Optional[List[str]]
    source_platform: Optional[str]
    source_url: Optional[str]
    tags: Optional[List[str]]
    tool_type: Optional[str]
    status: str
    is_high_potential: bool
    discovered_at: datetime
    created_at: datetime
    updated_at: datetime

class DemandUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    overall_score: Optional[float] = None
    status: Optional[str] = None
    is_high_potential: Optional[bool] = None
    tags: Optional[List[str]] = None

class DemandStats(BaseModel):
    total_demands: int
    high_potential_count: int
    avg_overall_score: float
    by_tool_type: dict
    by_status: dict
    recent_demands: List[DemandResponse]

@router.get("/", response_model=List[DemandResponse])
def get_demands(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    min_score: Optional[float] = Query(None, ge=0, le=10),
    tool_type: Optional[str] = None,
    status: Optional[str] = None,
    is_high_potential: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取需求列表"""
    try:
        query = db.query(Demand)
        
        # 应用筛选条件
        if min_score is not None:
            query = query.filter(Demand.overall_score >= min_score)
        
        if tool_type:
            query = query.filter(Demand.tool_type == tool_type)
        
        if status:
            query = query.filter(Demand.status == status)
        
        if is_high_potential is not None:
            query = query.filter(Demand.is_high_potential == is_high_potential)
        
        # 按评分降序排序
        demands = query.order_by(Demand.overall_score.desc()).offset(skip).limit(limit).all()
        
        logger.info(f"Retrieved {len(demands)} demands")
        return demands
        
    except Exception as e:
        logger.error(f"Error getting demands: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{demand_id}", response_model=DemandResponse)
def get_demand(demand_id: str, db: Session = Depends(get_db)):
    """获取单个需求详情"""
    try:
        demand = db.query(Demand).filter(Demand.id == demand_id).first()
        
        if not demand:
            raise HTTPException(status_code=404, detail="Demand not found")
        
        return demand
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting demand {demand_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=DemandResponse, status_code=status.HTTP_201_CREATED)
def create_demand(demand_data: DemandCreate, db: Session = Depends(get_db)):
    """创建新需求"""
    try:
        # 转换Pydantic模型为字典
        demand_dict = demand_data.dict()
        
        # 创建需求实例
        demand = Demand(**demand_dict)
        
        # 保存到数据库
        db.add(demand)
        db.commit()
        db.refresh(demand)
        
        logger.info(f"Created new demand: {demand.id} - {demand.title}")
        return demand
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating demand: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{demand_id}", response_model=DemandResponse)
def update_demand(demand_id: str, demand_update: DemandUpdate, db: Session = Depends(get_db)):
    """更新需求"""
    try:
        demand = db.query(Demand).filter(Demand.id == demand_id).first()
        
        if not demand:
            raise HTTPException(status_code=404, detail="Demand not found")
        
        # 更新字段
        update_data = demand_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(demand, field, value)
        
        db.commit()
        db.refresh(demand)
        
        logger.info(f"Updated demand: {demand_id}")
        return demand
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating demand {demand_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{demand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_demand(demand_id: str, db: Session = Depends(get_db)):
    """删除需求"""
    try:
        demand = db.query(Demand).filter(Demand.id == demand_id).first()
        
        if not demand:
            raise HTTPException(status_code=404, detail="Demand not found")
        
        db.delete(demand)
        db.commit()
        
        logger.info(f"Deleted demand: {demand_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting demand {demand_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/stats/summary", response_model=DemandStats)
def get_demand_stats(db: Session = Depends(get_db)):
    """获取需求统计信息"""
    try:
        # 总需求数
        total_demands = db.query(Demand).count()
        
        # 高潜力需求数
        high_potential_count = db.query(Demand).filter(Demand.is_high_potential == True).count()
        
        # 平均评分
        avg_score_result = db.query(db.func.avg(Demand.overall_score)).scalar()
        avg_overall_score = float(avg_score_result) if avg_score_result else 0.0
        
        # 按工具类型统计
        tool_type_counts = {}
        tool_types = db.query(Demand.tool_type).distinct().all()
        for tool_type in tool_types:
            if tool_type[0]:
                count = db.query(Demand).filter(Demand.tool_type == tool_type[0]).count()
                tool_type_counts[tool_type[0]] = count
        
        # 按状态统计
        status_counts = {}
        statuses = db.query(Demand.status).distinct().all()
        for status in statuses:
            if status[0]:
                count = db.query(Demand).filter(Demand.status == status[0]).count()
                status_counts[status[0]] = count
        
        # 最近的需求
        recent_demands = db.query(Demand).order_by(Demand.created_at.desc()).limit(10).all()
        
        return DemandStats(
            total_demands=total_demands,
            high_potential_count=high_potential_count,
            avg_overall_score=avg_overall_score,
            by_tool_type=tool_type_counts,
            by_status=status_counts,
            recent_demands=recent_demands
        )
        
    except Exception as e:
        logger.error(f"Error getting demand stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/search/", response_model=List[DemandResponse])
def search_demands(
    q: str = Query(..., min_length=2, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """搜索需求"""
    try:
        # 简单的全文搜索（在实际项目中应该使用全文搜索引擎）
        demands = db.query(Demand).filter(
            Demand.title.ilike(f"%{q}%") | 
            Demand.description.ilike(f"%{q}%") |
            Demand.problem.ilike(f"%{q}%")
        ).order_by(Demand.overall_score.desc()).limit(50).all()
        
        logger.info(f"Search for '{q}' returned {len(demands)} results")
        return demands
        
    except Exception as e:
        logger.error(f"Error searching demands: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")