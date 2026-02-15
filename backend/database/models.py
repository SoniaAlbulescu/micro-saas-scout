from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class Demand(Base):
    """需求表 - 存储挖掘到的工具需求"""
    __tablename__ = "demands"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    problem = Column(Text, nullable=False)
    
    # 用户画像
    user_role = Column(String(200))
    company_size = Column(String(100))
    tech_level = Column(String(100))
    budget_range = Column(String(100))
    
    # 使用场景
    scenario = Column(Text)
    
    # 痛点分析
    pain_points = Column(JSON)  # 存储为JSON数组
    
    # 现有解决方案
    existing_solutions = Column(JSON)
    
    # 付费信号
    pricing_signals = Column(JSON)
    
    # 市场数据
    search_volume = Column(Integer, default=0)
    competitor_users = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)
    
    # 技术评估
    technical_complexity = Column(String(50))  # low, medium, high
    dev_time_weeks = Column(Integer)
    main_tech_stack = Column(JSON)
    
    # 评分
    demand_strength_score = Column(Float, default=0.0)
    market_size_score = Column(Float, default=0.0)
    willingness_to_pay_score = Column(Float, default=0.0)
    technical_feasibility_score = Column(Float, default=0.0)
    passive_income_fit_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # 推荐信息
    recommended_pricing = Column(String(100))
    mvp_features = Column(JSON)
    
    # 来源信息
    source_platform = Column(String(100))
    source_url = Column(String(500))
    discovered_at = Column(DateTime, default=datetime.utcnow)
    
    # 标签和分类
    tags = Column(JSON)
    tool_type = Column(String(100))
    
    # 状态
    status = Column(String(50), default="new")  # new, reviewed, validated, rejected
    is_high_potential = Column(Boolean, default=False)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Source(Base):
    """数据源表 - 存储要监控的数据源"""
    __tablename__ = "sources"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    platform = Column(String(100), nullable=False)  # hackernews, reddit, producthunt, etc.
    url = Column(String(500))
    api_endpoint = Column(String(500))
    
    # 配置
    config = Column(JSON)
    is_active = Column(Boolean, default=True)
    crawl_interval_hours = Column(Integer, default=24)
    
    # 统计
    last_crawled_at = Column(DateTime)
    total_demands_found = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AnalysisResult(Base):
    """分析结果表 - 存储系统分析结果"""
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    demand_id = Column(String, ForeignKey("demands.id"), nullable=False)
    
    # 分析维度
    sentiment_score = Column(Float)
    urgency_score = Column(Float)
    uniqueness_score = Column(Float)
    
    # 关键词提取
    keywords = Column(JSON)
    entities = Column(JSON)
    
    # 分类
    category = Column(String(100))
    subcategory = Column(String(100))
    
    # 时间戳
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemStats(Base):
    """系统统计表"""
    __tablename__ = "system_stats"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    date = Column(DateTime, default=datetime.utcnow)
    
    # 需求统计
    total_demands = Column(Integer, default=0)
    new_demands_today = Column(Integer, default=0)
    high_potential_demands = Column(Integer, default=0)
    
    # 来源统计
    active_sources = Column(Integer, default=0)
    successful_crawls_today = Column(Integer, default=0)
    
    # 评分统计
    avg_overall_score = Column(Float, default=0.0)
    avg_pricing_potential = Column(Float, default=0.0)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)