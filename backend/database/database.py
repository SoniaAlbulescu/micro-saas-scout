import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
import logging
from .models import Base

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """数据库连接管理器"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """初始化数据库连接"""
        try:
            # 从环境变量获取数据库URL
            database_url = os.getenv("DATABASE_URL")
            
            if not database_url:
                logger.error("DATABASE_URL environment variable is not set")
                # 使用本地测试URL（仅用于开发）
                database_url = "postgresql://postgres:password@localhost/micro_saas"
                logger.warning(f"Using default database URL: {database_url}")
            
            # 创建数据库引擎
            self.engine = create_engine(
                database_url,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # 设置为True可查看SQL日志
            )
            
            # 创建会话工厂
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info("Database connection initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
    
    def create_tables(self):
        """创建所有表（如果不存在）"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {str(e)}")
            raise
    
    @contextmanager
    def get_session(self):
        """获取数据库会话的上下文管理器"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {str(e)}")
            raise
        finally:
            session.close()
    
    def test_connection(self):
        """测试数据库连接"""
        try:
            with self.get_session() as session:
                # 执行简单的查询测试连接
                session.execute("SELECT 1")
                logger.info("Database connection test passed")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {str(e)}")
            return False
    
    def get_stats(self):
        """获取数据库统计信息"""
        try:
            with self.get_session() as session:
                # 获取表统计
                from .models import Demand, Source
                
                total_demands = session.query(Demand).count()
                total_sources = session.query(Source).count()
                active_sources = session.query(Source).filter(Source.is_active == True).count()
                
                return {
                    "total_demands": total_demands,
                    "total_sources": total_sources,
                    "active_sources": active_sources,
                    "database_url": os.getenv("DATABASE_URL", "not set")[:50] + "..."  # 隐藏部分URL
                }
        except Exception as e:
            logger.error(f"Failed to get database stats: {str(e)}")
            return {}

# 创建全局数据库实例
db = Database()

# 导出常用函数
def get_db():
    """获取数据库会话（用于依赖注入）"""
    with db.get_session() as session:
        yield session

def init_db():
    """初始化数据库（创建表）"""
    db.create_tables()
    return db.test_connection()

if __name__ == "__main__":
    # 测试数据库连接
    if init_db():
        print("✅ Database initialized successfully")
        stats = db.get_stats()
        print(f"📊 Database stats: {stats}")
    else:
        print("❌ Database initialization failed")