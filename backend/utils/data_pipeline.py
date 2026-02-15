import logging
from datetime import datetime
from typing import List, Dict, Optional
import time

from backend.database.database import db
from backend.database.models import Demand, Source
from backend.crawlers.hackernews_crawler import HackerNewsCrawler
from backend.analysis.demand_analyzer import DemandAnalyzer

logger = logging.getLogger(__name__)

class DataPipeline:
    """数据管道 - 连接爬虫、分析和数据库"""
    
    def __init__(self):
        self.crawler = HackerNewsCrawler()
        self.analyzer = DemandAnalyzer()
        self.stats = {
            "total_processed": 0,
            "successful_saves": 0,
            "failed_saves": 0,
            "last_run": None,
            "run_duration": 0
        }
    
    def run_hackernews_pipeline(self, max_posts: int = 30) -> Dict:
        """运行完整的HackerNews数据管道"""
        logger.info(f"Starting HackerNews data pipeline (max_posts: {max_posts})")
        
        start_time = time.time()
        
        try:
            # 1. 爬取数据
            crawl_result = self.crawler.crawl(max_posts=max_posts)
            posts = crawl_result.get("posts", [])
            raw_demands = crawl_result.get("demands", [])
            
            logger.info(f"Crawled {len(posts)} posts, found {len(raw_demands)} potential demands")
            
            # 2. 分析需求
            analyzed_demands = []
            for raw_demand in raw_demands:
                try:
                    analysis = self.analyzer.analyze_demand(raw_demand)
                    
                    if "error" not in analysis:
                        analyzed_demand = {
                            "raw": raw_demand,
                            "analysis": analysis,
                            "recommendations": self.analyzer.generate_recommendations(analysis)
                        }
                        analyzed_demands.append(analyzed_demand)
                        
                except Exception as e:
                    logger.warning(f"Error analyzing demand: {str(e)}")
                    continue
            
            logger.info(f"Successfully analyzed {len(analyzed_demands)} demands")
            
            # 3. 保存到数据库
            saved_count = 0
            for analyzed_demand in analyzed_demands:
                try:
                    if self._save_to_database(analyzed_demand):
                        saved_count += 1
                except Exception as e:
                    logger.warning(f"Error saving demand to database: {str(e)}")
                    continue
            
            # 4. 更新统计
            self.stats["total_processed"] += len(analyzed_demands)
            self.stats["successful_saves"] += saved_count
            self.stats["failed_saves"] += len(analyzed_demands) - saved_count
            self.stats["last_run"] = datetime.utcnow().isoformat()
            self.stats["run_duration"] = time.time() - start_time
            
            # 5. 更新数据源状态
            self._update_source_status("hackernews", len(analyzed_demands))
            
            result = {
                "status": "success",
                "stats": {
                    "posts_crawled": len(posts),
                    "demands_found": len(raw_demands),
                    "demands_analyzed": len(analyzed_demands),
                    "demands_saved": saved_count,
                    "pipeline_duration_seconds": self.stats["run_duration"]
                },
                "crawl_stats": crawl_result.get("stats", {}),
                "pipeline_stats": self.stats.copy()
            }
            
            logger.info(f"Pipeline completed: {result['stats']}")
            return result
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "pipeline_duration_seconds": time.time() - start_time
            }
    
    def _save_to_database(self, analyzed_demand: Dict) -> bool:
        """保存分析后的需求到数据库"""
        try:
            raw = analyzed_demand["raw"]
            analysis = analyzed_demand["analysis"]
            recommendations = analyzed_demand["recommendations"]
            
            # 构建需求数据
            demand_data = {
                "title": raw.get("source_post", {}).get("title", "Untitled Demand")[:500],
                "description": f"Extracted from {analysis['source_info']['platform']}: {raw.get('extracted_text', '')}"[:2000],
                "problem": raw.get("extracted_text", "No problem description"),
                
                # 用户画像（基于分析）
                "user_role": "developer/tech_user",  # 可以从文本中提取
                "company_size": "individual/small_team",
                "tech_level": "intermediate",
                "budget_range": self._get_budget_range(analysis.get("payment_potential")),
                
                # 使用场景
                "scenario": f"Found on {analysis['source_info']['platform']} discussion",
                
                # 痛点分析
                "pain_points": ["Manual process", "Time consuming", "Lack of existing solutions"],
                
                # 现有解决方案
                "existing_solutions": ["Manual work", "Complex existing tools"],
                
                # 付费信号
                "pricing_signals": [f"Payment potential: {analysis.get('payment_potential', 'medium')}"],
                
                # 市场数据（估算）
                "search_volume": self._estimate_search_volume(analysis.get("tool_type")),
                "competitor_users": self._estimate_competitor_users(analysis.get("tool_type")),
                "growth_rate": self._estimate_growth_rate(analysis.get("tool_type")),
                
                # 技术评估
                "technical_complexity": analysis.get("technical_complexity", "medium"),
                "dev_time_weeks": recommendations.get("time_estimate_weeks", 4),
                "main_tech_stack": recommendations.get("suggested_tech_stack", []),
                
                # 评分
                "demand_strength_score": analysis["scores"].get("demand_strength", 5.0),
                "market_size_score": analysis["scores"].get("market_size", 5.0),
                "willingness_to_pay_score": analysis["scores"].get("payment_willingness", 5.0),
                "technical_feasibility_score": analysis["scores"].get("technical_feasibility", 5.0),
                "passive_income_fit_score": analysis["scores"].get("passive_income_fit", 5.0),
                "overall_score": analysis["scores"].get("overall", 5.0),
                
                # 推荐信息
                "recommended_pricing": recommendations.get("recommended_pricing", "$15-25/month"),
                "mvp_features": recommendations.get("mvp_features", []),
                
                # 来源信息
                "source_platform": analysis["source_info"]["platform"],
                "source_url": analysis["source_info"]["post_url"],
                "discovered_at": datetime.utcnow(),
                
                # 标签和分类
                "tags": analysis.get("keywords", [])[:5],
                "tool_type": analysis.get("tool_type", "unknown"),
                
                # 状态
                "status": "new",
                "is_high_potential": analysis["scores"].get("overall", 0) >= 7.0
            }
            
            # 保存到数据库
            with db.get_session() as session:
                demand = Demand(**demand_data)
                session.add(demand)
                session.commit()
                
                logger.debug(f"Saved demand to database: {demand.id} - {demand.title[:50]}...")
                return True
                
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            return False
    
    def _update_source_status(self, platform: str, demands_found: int):
        """更新数据源状态"""
        try:
            with db.get_session() as session:
                # 查找或创建数据源记录
                source = session.query(Source).filter(
                    Source.platform == platform
                ).first()
                
                if not source:
                    source = Source(
                        name=f"{platform.capitalize()} Crawler",
                        platform=platform,
                        url=self._get_platform_url(platform),
                        is_active=True,
                        crawl_interval_hours=24
                    )
                    session.add(source)
                
                # 更新统计
                source.last_crawled_at = datetime.utcnow()
                source.total_demands_found += demands_found
                
                if demands_found > 0:
                    source.success_rate = min(100.0, source.success_rate + 10.0)
                else:
                    source.success_rate = max(0.0, source.success_rate - 5.0)
                
                session.commit()
                logger.debug(f"Updated source status for {platform}")
                
        except Exception as e:
            logger.warning(f"Error updating source status: {str(e)}")
    
    def _get_budget_range(self, payment_potential: str) -> str:
        """根据付费潜力获取预算范围"""
        ranges = {
            'high': '$20-50/month',
            'medium': '$10-30/month',
            'low': '$5-15/month'
        }
        return ranges.get(payment_potential, '$10-30/month')
    
    def _estimate_search_volume(self, tool_type: str) -> int:
        """估算搜索量"""
        base_volumes = {
            'web_app': 5000,
            'browser_extension': 3000,
            'api_service': 2000,
            'mobile_app': 4000,
            'automation': 2500,
            'analytics': 1800,
            'cli_tool': 800,
            'desktop_app': 1200,
            'unknown': 1500
        }
        return base_volumes.get(tool_type, 1000)
    
    def _estimate_competitor_users(self, tool_type: str) -> int:
        """估算竞品用户数"""
        base_users = {
            'web_app': 10000,
            'browser_extension': 5000,
            'api_service': 3000,
            'mobile_app': 8000,
            'automation': 4000,
            'analytics': 2500,
            'cli_tool': 1000,
            'desktop_app': 2000,
            'unknown': 2000
        }
        return base_users.get(tool_type, 1500)
    
    def _estimate_growth_rate(self, tool_type: str) -> float:
        """估算增长率"""
        base_rates = {
            'web_app': 25.0,
            'browser_extension': 20.0,
            'api_service': 30.0,
            'mobile_app': 22.0,
            'automation': 35.0,
            'analytics': 28.0,
            'cli_tool': 15.0,
            'desktop_app': 12.0,
            'unknown': 20.0
        }
        return base_rates.get(tool_type, 20.0)
    
    def _get_platform_url(self, platform: str) -> str:
        """获取平台URL"""
        urls = {
            'hackernews': 'https://news.ycombinator.com',
            'reddit': 'https://reddit.com',
            'producthunt': 'https://producthunt.com'
        }
        return urls.get(platform, '')
    
    def get_pipeline_stats(self) -> Dict:
        """获取管道统计信息"""
        return self.stats.copy()
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total_processed": 0,
            "successful_saves": 0,
            "failed_saves": 0,
            "last_run": None,
            "run_duration": 0
        }

# 使用示例
if __name__ == "__main__":
    import json
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建数据管道
    pipeline = DataPipeline()
    
    print("🚀 Starting Micro SaaS Scout Data Pipeline...")
    print("=" * 50)
    
    # 运行管道
    result = pipeline.run_hackernews_pipeline(max_posts=20)
    
    print("\n📊 Pipeline Results:")
    print(json.dumps(result, indent=2))
    
    if result["status"] == "success":
        stats = result["stats"]
        print(f"\n✅ Pipeline completed successfully!")
        print(f"   • Posts crawled: {stats['posts_crawled']}")
        print(f"   • Demands found: {stats['demands_found']}")
        print(f"   • Demands saved: {stats['demands_saved']}")
        print(f"   • Duration: {stats['pipeline_duration_seconds']:.2f} seconds")
    else:
        print(f"\n❌ Pipeline failed: {result.get('error', 'Unknown error')}")