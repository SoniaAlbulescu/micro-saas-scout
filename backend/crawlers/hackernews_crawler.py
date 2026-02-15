import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from typing import List, Dict, Optional
import time
import re

logger = logging.getLogger(__name__)

class HackerNewsCrawler:
    """Hacker News爬虫 - 抓取技术工具需求"""
    
    BASE_URL = "https://news.ycombinator.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
    
    def fetch_show_hn(self, limit: int = 30) -> List[Dict]:
        """抓取Show HN帖子（新产品展示）"""
        try:
            logger.info(f"Fetching Show HN posts (limit: {limit})")
            
            url = f"{self.BASE_URL}/show"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 解析帖子
            posts = []
            rows = soup.select('tr.athing')
            
            for i, row in enumerate(rows[:limit]):
                try:
                    post = self._parse_post(row)
                    if post:
                        posts.append(post)
                        logger.debug(f"Parsed post: {post['title'][:50]}...")
                except Exception as e:
                    logger.warning(f"Failed to parse post {i}: {str(e)}")
                    continue
            
            logger.info(f"Successfully fetched {len(posts)} Show HN posts")
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching Show HN: {str(e)}")
            return []
    
    def fetch_ask_hn(self, limit: int = 30) -> List[Dict]:
        """抓取Ask HN帖子（问题讨论）"""
        try:
            logger.info(f"Fetching Ask HN posts (limit: {limit})")
            
            url = f"{self.BASE_URL}/ask"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            posts = []
            rows = soup.select('tr.athing')
            
            for i, row in enumerate(rows[:limit]):
                try:
                    post = self._parse_post(row)
                    if post:
                        posts.append(post)
                except Exception as e:
                    logger.warning(f"Failed to parse Ask HN post {i}: {str(e)}")
                    continue
            
            logger.info(f"Successfully fetched {len(posts)} Ask HN posts")
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching Ask HN: {str(e)}")
            return []
    
    def _parse_post(self, row) -> Optional[Dict]:
        """解析单个帖子"""
        try:
            # 提取标题和链接
            title_elem = row.select_one('a.titlelink')
            if not title_elem:
                return None
            
            title = title_elem.text.strip()
            url = title_elem.get('href', '')
            
            # 处理相对链接
            if url.startswith('item?'):
                url = f"{self.BASE_URL}/{url}"
            
            # 提取分数和评论数
            subtext_row = row.find_next_sibling('tr')
            if not subtext_row:
                return None
            
            subtext = subtext_row.select_one('.subtext')
            if not subtext:
                return None
            
            # 提取分数
            score_elem = subtext.select_one('.score')
            score = 0
            if score_elem:
                score_text = score_elem.text.strip()
                match = re.search(r'(\d+)', score_text)
                if match:
                    score = int(match.group(1))
            
            # 提取评论数
            comments_elem = subtext.find_all('a')[-1]
            comments = 0
            if comments_elem and 'comment' in comments_elem.text:
                comments_text = comments_elem.text.strip()
                match = re.search(r'(\d+)', comments_text)
                if match:
                    comments = int(match.group(1))
            
            # 提取用户和时间
            user_elem = subtext.select_one('.hnuser')
            user = user_elem.text.strip() if user_elem else "anonymous"
            
            time_elem = subtext.select_one('.age')
            posted_time = time_elem.text.strip() if time_elem else ""
            
            # 构建帖子数据
            post_data = {
                "title": title,
                "url": url,
                "score": score,
                "comments": comments,
                "user": user,
                "posted_time": posted_time,
                "platform": "hackernews",
                "crawled_at": datetime.utcnow().isoformat(),
                "type": self._classify_post(title)
            }
            
            return post_data
            
        except Exception as e:
            logger.warning(f"Error parsing post: {str(e)}")
            return None
    
    def _classify_post(self, title: str) -> str:
        """根据标题分类帖子类型"""
        title_lower = title.lower()
        
        # 工具相关关键词
        tool_keywords = [
            'tool', 'app', 'website', 'platform', 'service', 'api',
            'library', 'framework', 'cli', 'extension', 'plugin',
            'dashboard', 'analytics', 'monitor', 'automation'
        ]
        
        # 问题相关关键词
        problem_keywords = [
            'how to', 'why', 'what', 'which', 'help', 'advice',
            'recommend', 'suggest', 'looking for', 'need', 'want',
            'problem', 'issue', 'challenge', 'pain', 'annoying'
        ]
        
        # 检查是否包含工具关键词
        if any(keyword in title_lower for keyword in tool_keywords):
            return "tool_announcement"
        
        # 检查是否包含问题关键词
        if any(keyword in title_lower for keyword in problem_keywords):
            return "problem_discussion"
        
        return "other"
    
    def extract_demands_from_post(self, post: Dict) -> List[Dict]:
        """从帖子中提取潜在需求"""
        demands = []
        
        try:
            title = post.get('title', '').lower()
            
            # 识别潜在需求模式
            demand_patterns = [
                # "I built X to solve Y"
                (r'(built|created|made)\s+(?:a\s+)?(.+?)\s+(?:to|for)\s+(?:solve|fix|help|automate)\s+(.+)', 'tool_solution'),
                # "Looking for a tool that does X"
                (r'looking for (?:a\s+)?(.+?)\s+(?:that|which)\s+(.+)', 'tool_request'),
                # "Is there a tool for X?"
                (r'is there (?:a\s+)?(.+?)\s+for\s+(.+)', 'tool_inquiry'),
                # "How do you handle X?"
                (r'how do you (?:handle|manage|deal with|solve)\s+(.+)', 'problem_question'),
                # "The problem with X is Y"
                (r'the problem with (.+?)\s+is\s+(.+)', 'problem_statement'),
            ]
            
            for pattern, demand_type in demand_patterns:
                match = re.search(pattern, title, re.IGNORECASE)
                if match:
                    demand = {
                        "source_post": post,
                        "demand_type": demand_type,
                        "extracted_text": title,
                        "confidence": 0.7,  # 置信度评分
                        "extracted_at": datetime.utcnow().isoformat(),
                        "patterns_found": [pattern]
                    }
                    demands.append(demand)
                    logger.debug(f"Found demand pattern: {demand_type} in '{title[:50]}...'")
            
            # 如果帖子有很多评论，可能包含更多需求讨论
            if post.get('comments', 0) > 10:
                # 这里可以添加抓取评论的逻辑
                pass
            
            return demands
            
        except Exception as e:
            logger.error(f"Error extracting demands from post: {str(e)}")
            return []
    
    def crawl(self, max_posts: int = 50) -> Dict:
        """执行完整的爬取流程"""
        logger.info(f"Starting HackerNews crawl (max_posts: {max_posts})")
        
        start_time = time.time()
        
        try:
            # 抓取数据
            show_hn_posts = self.fetch_show_hn(limit=max_posts//2)
            ask_hn_posts = self.fetch_ask_hn(limit=max_posts//2)
            
            all_posts = show_hn_posts + ask_hn_posts
            
            # 提取需求
            all_demands = []
            for post in all_posts:
                demands = self.extract_demands_from_post(post)
                all_demands.extend(demands)
            
            # 统计信息
            stats = {
                "total_posts": len(all_posts),
                "show_hn_posts": len(show_hn_posts),
                "ask_hn_posts": len(ask_hn_posts),
                "total_demands_found": len(all_demands),
                "crawl_duration_seconds": time.time() - start_time,
                "crawled_at": datetime.utcnow().isoformat(),
                "platform": "hackernews"
            }
            
            logger.info(f"Crawl completed: {stats}")
            
            return {
                "posts": all_posts,
                "demands": all_demands,
                "stats": stats
            }
            
        except Exception as e:
            logger.error(f"Crawl failed: {str(e)}")
            return {
                "posts": [],
                "demands": [],
                "stats": {
                    "error": str(e),
                    "crawl_duration_seconds": time.time() - start_time,
                    "crawled_at": datetime.utcnow().isoformat()
                }
            }

# 使用示例
if __name__ == "__main__":
    import json
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建爬虫实例
    crawler = HackerNewsCrawler()
    
    # 执行爬取
    result = crawler.crawl(max_posts=20)
    
    # 打印结果
    print(f"📊 Crawl Stats:")
    print(json.dumps(result["stats"], indent=2))
    
    print(f"\n📝 Found {len(result['demands'])} potential demands:")
    for i, demand in enumerate(result["demands"][:5], 1):
        print(f"{i}. Type: {demand['demand_type']}")
        print(f"   Text: {demand['extracted_text'][:100]}...")
        print(f"   Confidence: {demand['confidence']}")
        print()
    
    if result["demands"]:
        print(f"✅ Successfully extracted {len(result['demands'])} potential tool demands from HackerNews!")
    else:
        print("ℹ️ No tool demands found in this crawl.")