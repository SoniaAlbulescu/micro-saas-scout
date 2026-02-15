import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

# 下载NLTK数据（第一次运行时需要）
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class DemandAnalyzer:
    """需求分析引擎 - 分析提取的需求并评分"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # 关键词库
        self.tool_keywords = {
            'browser_extension': ['extension', 'chrome', 'firefox', 'browser', 'plugin', 'addon'],
            'api_service': ['api', 'rest', 'graphql', 'endpoint', 'integration'],
            'cli_tool': ['cli', 'command line', 'terminal', 'shell', 'script'],
            'mobile_app': ['app', 'mobile', 'ios', 'android', 'phone'],
            'desktop_app': ['desktop', 'windows', 'mac', 'linux', 'application'],
            'web_app': ['web', 'website', 'saas', 'cloud', 'online'],
            'automation': ['automate', 'automation', 'bot', 'robot', 'schedule'],
            'analytics': ['analytics', 'dashboard', 'metrics', 'report', 'statistics'],
            'monitoring': ['monitor', 'alert', 'notification', 'track', 'watch'],
            'productivity': ['productivity', 'efficiency', 'time', 'save', 'fast']
        }
        
        # 付费信号关键词
        self.payment_keywords = {
            'high': ['pay', 'price', 'cost', 'subscription', 'monthly', 'yearly', 
                    'premium', 'enterprise', 'business', 'professional', 'worth'],
            'medium': ['free', 'trial', 'freemium', 'basic', 'standard', 'affordable'],
            'low': ['open source', 'free', 'gratis', 'no cost', 'cheap']
        }
        
        # 技术复杂度关键词
        self.complexity_keywords = {
            'high': ['ai', 'machine learning', 'blockchain', 'real-time', 'scalable',
                    'distributed', 'complex', 'advanced', 'sophisticated'],
            'medium': ['database', 'api', 'integration', 'automation', 'dashboard',
                      'analytics', 'monitoring', 'scheduling'],
            'low': ['simple', 'basic', 'lightweight', 'minimal', 'straightforward']
        }
    
    def analyze_demand(self, raw_demand: Dict) -> Dict:
        """分析单个需求"""
        try:
            logger.info(f"Analyzing demand: {raw_demand.get('extracted_text', '')[:50]}...")
            
            # 提取文本
            text = raw_demand.get('extracted_text', '').lower()
            
            # 基础分析
            tool_type = self._classify_tool_type(text)
            payment_potential = self._assess_payment_potential(text)
            complexity = self._assess_complexity(text)
            
            # 提取关键词
            keywords = self._extract_keywords(text)
            
            # 评分
            scores = self._calculate_scores(text, tool_type, payment_potential, complexity)
            
            # 构建分析结果
            analysis = {
                "tool_type": tool_type,
                "payment_potential": payment_potential,
                "technical_complexity": complexity,
                "keywords": keywords,
                "scores": scores,
                "analyzed_at": datetime.utcnow().isoformat(),
                "confidence": raw_demand.get('confidence', 0.5),
                "source_info": {
                    "platform": raw_demand.get('source_post', {}).get('platform', 'unknown'),
                    "post_title": raw_demand.get('source_post', {}).get('title', ''),
                    "post_url": raw_demand.get('source_post', {}).get('url', '')
                }
            }
            
            logger.debug(f"Analysis completed: {analysis}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing demand: {str(e)}")
            return {
                "error": str(e),
                "analyzed_at": datetime.utcnow().isoformat()
            }
    
    def _classify_tool_type(self, text: str) -> str:
        """分类工具类型"""
        scores = {}
        
        for tool_type, keywords in self.tool_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            
            if score > 0:
                scores[tool_type] = score
        
        if scores:
            # 返回得分最高的类型
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return "unknown"
    
    def _assess_payment_potential(self, text: str) -> str:
        """评估付费潜力"""
        scores = {'high': 0, 'medium': 0, 'low': 0}
        
        for level, keywords in self.payment_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[level] += 1
        
        # 返回得分最高的级别
        max_level = max(scores.items(), key=lambda x: x[1])
        
        # 如果所有得分都为0，返回medium
        if max_level[1] == 0:
            return "medium"
        
        return max_level[0]
    
    def _assess_complexity(self, text: str) -> str:
        """评估技术复杂度"""
        scores = {'high': 0, 'medium': 0, 'low': 0}
        
        for level, keywords in self.complexity_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    scores[level] += 1
        
        max_level = max(scores.items(), key=lambda x: x[1])
        
        if max_level[1] == 0:
            return "medium"
        
        return max_level[0]
    
    def _extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """提取关键词"""
        try:
            # 分词
            tokens = word_tokenize(text.lower())
            
            # 移除停用词和标点
            filtered_tokens = [
                token for token in tokens 
                if token.isalnum() and token not in self.stop_words
            ]
            
            # 统计词频
            word_freq = Counter(filtered_tokens)
            
            # 返回最常见的词
            return [word for word, _ in word_freq.most_common(top_n)]
            
        except Exception as e:
            logger.warning(f"Error extracting keywords: {str(e)}")
            return []
    
    def _calculate_scores(self, text: str, tool_type: str, payment_potential: str, complexity: str) -> Dict:
        """计算各项评分"""
        
        # 1. 需求强度评分 (0-10)
        # 基于文本长度、特定关键词等
        demand_strength = 5.0  # 基础分
        
        # 增加强度的关键词
        strong_keywords = ['need', 'want', 'must', 'essential', 'critical', 'urgent']
        for keyword in strong_keywords:
            if keyword in text:
                demand_strength += 0.5
        
        # 文本长度影响
        word_count = len(text.split())
        if word_count > 50:
            demand_strength += 1.0
        elif word_count < 10:
            demand_strength -= 1.0
        
        demand_strength = max(0, min(10, demand_strength))
        
        # 2. 市场规模评分 (0-10)
        # 基于工具类型和通用性
        market_size = 6.0
        
        # 通用工具类型有更大市场
        broad_market_tools = ['web_app', 'browser_extension', 'mobile_app', 'productivity']
        if tool_type in broad_market_tools:
            market_size += 2.0
        
        # 小众工具类型市场较小
        niche_tools = ['cli_tool', 'desktop_app']
        if tool_type in niche_tools:
            market_size -= 1.0
        
        market_size = max(0, min(10, market_size))
        
        # 3. 付费意愿评分 (0-10)
        payment_willingness = {
            'high': 8.0,
            'medium': 5.0,
            'low': 2.0
        }.get(payment_potential, 5.0)
        
        # 4. 技术可行性评分 (0-10)
        technical_feasibility = {
            'low': 9.0,   # 低复杂度 = 高可行性
            'medium': 6.0,
            'high': 3.0   # 高复杂度 = 低可行性
        }.get(complexity, 6.0)
        
        # 5. 被动收入适配度评分 (0-10)
        passive_income_fit = 5.0
        
        # 适合被动收入的特性
        passive_friendly_keywords = ['subscription', 'saas', 'cloud', 'automation', 'api']
        for keyword in passive_friendly_keywords:
            if keyword in text:
                passive_income_fit += 1.0
        
        # 工具类型影响
        passive_friendly_tools = ['web_app', 'api_service', 'automation', 'analytics']
        if tool_type in passive_friendly_tools:
            passive_income_fit += 2.0
        
        passive_income_fit = max(0, min(10, passive_income_fit))
        
        # 6. 综合评分 (加权平均)
        weights = {
            'demand_strength': 0.25,
            'market_size': 0.20,
            'payment_willingness': 0.25,
            'technical_feasibility': 0.15,
            'passive_income_fit': 0.15
        }
        
        overall_score = (
            demand_strength * weights['demand_strength'] +
            market_size * weights['market_size'] +
            payment_willingness * weights['payment_willingness'] +
            technical_feasibility * weights['technical_feasibility'] +
            passive_income_fit * weights['passive_income_fit']
        )
        
        return {
            "demand_strength": round(demand_strength, 1),
            "market_size": round(market_size, 1),
            "payment_willingness": round(payment_willingness, 1),
            "technical_feasibility": round(technical_feasibility, 1),
            "passive_income_fit": round(passive_income_fit, 1),
            "overall": round(overall_score, 1)
        }
    
    def generate_recommendations(self, analysis: Dict) -> Dict:
        """生成推荐信息"""
        scores = analysis.get('scores', {})
        tool_type = analysis.get('tool_type', 'unknown')
        
        # 推荐定价
        payment_potential = analysis.get('payment_potential', 'medium')
        base_price = {
            'high': 29.99,
            'medium': 14.99,
            'low': 4.99
        }.get(payment_potential, 14.99)
        
        # 根据评分调整
        overall_score = scores.get('overall', 5.0)
        price_multiplier = overall_score / 10.0 * 1.5  # 0.75-1.5倍
        
        recommended_price = round(base_price * price_multiplier, 2)
        
        # MVP功能建议
        mvp_features = self._suggest_mvp_features(tool_type)
        
        # 技术栈建议
        tech_stack = self._suggest_tech_stack(tool_type, analysis.get('technical_complexity', 'medium'))
        
        return {
            "recommended_pricing": f"${recommended_price}/month",
            "mvp_features": mvp_features,
            "suggested_tech_stack": tech_stack,
            "time_estimate_weeks": self._estimate_dev_time(analysis.get('technical_complexity', 'medium')),
            "priority": "high" if overall_score >= 7.0 else "medium" if overall_score >= 5.0 else "low"
        }
    
    def _suggest_mvp_features(self, tool_type: str) -> List[str]:
        """根据工具类型建议MVP功能"""
        feature_templates = {
            'browser_extension': [
                "Basic content injection/modification",
                "Simple popup interface",
                "Local storage for user preferences",
                "Content script for target websites"
            ],
            'api_service': [
                "RESTful API endpoints",
                "Authentication (API keys)",
                "Rate limiting",
                "Basic documentation"
            ],
            'web_app': [
                "User authentication",
                "Core functionality dashboard",
                "Basic settings page",
                "Responsive design"
            ],
            'automation': [
                "Schedule tasks",
                "Basic error handling",
                "Notification system",
                "Task history/logging"
            ]
        }
        
        return feature_templates.get(tool_type, [
            "Core functionality",
            "User authentication",
            "Basic UI/UX",
            "Error handling"
        ])
    
    def _suggest_tech_stack(self, tool_type: str, complexity: str) -> List[str]:
        """建议技术栈"""
        stacks = {
            'browser_extension': ["JavaScript", "HTML/CSS", "Chrome Extension API"],
            'api_service': ["Python/FastAPI", "PostgreSQL", "Docker"],
            'web_app': ["React/Next.js", "Node.js", "PostgreSQL", "Tailwind CSS"],
            'cli_tool': ["Python", "Click library", "Docker"],
            'mobile_app': ["React Native", "Firebase", "Expo"]
        }
        
        base_stack = stacks.get(tool_type, ["Python", "React", "PostgreSQL"])
        
        # 根据复杂度添加技术
        if complexity == 'high':
            base_stack.extend(["Docker", "Redis", "Celery", "Monitoring"])
        elif complexity == 'medium':
            base_stack.extend(["Docker", "Basic logging"])
        
        return base_stack
    
    def _estimate_dev_time(self, complexity: str) -> int:
        """估算开发时间（周）"""
        return {
            'low': 2,
            'medium': 4,
            'high': 8
        }.get(complexity, 4)

# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建分析器
    analyzer = DemandAnalyzer()
    
    # 测试需求
    test_demand = {
        "extracted_text": "I need a tool to automatically sync Google Sheets data to Notion. Currently doing it manually and it takes hours every week. Would pay $20/month for a reliable solution.",
        "confidence": 0.8,
        "source_post": {
            "platform": "hackernews",
            "title": "Looking for Google Sheets to Notion sync tool",
            "url": "https://news.ycombinator.com/item?id=123456"
        }
    }
    
    # 分析需求
    analysis = analyzer.analyze_demand(test_demand)
    
    print("🔍 Demand Analysis Results:")
    print(f"Tool Type: {analysis.get('tool_type')}")
    print(f"Payment Potential: {analysis.get('payment_potential')}")
    print(f"Technical Complexity: {analysis.get('technical_complexity')}")
    print(f"Keywords: {', '.join(analysis.get('keywords', [])[:5])}")
    
    print("\n📊 Scores:")
    scores = analysis.get('scores', {})
    for key, value in scores.items():
        print(f"  {key}: {value}/10")
    
    # 生成推荐
    recommendations = analyzer.generate_recommendations(analysis)
    
    print("\n💡 Recommendations:")
    print(f"Pricing: {recommendations.get('recommended_pricing')}")
    print(f"Dev Time: {recommendations.get('time_estimate_weeks')} weeks")
    print(f"Priority: {recommendations.get('priority')}")
    print(f"Tech Stack: {', '.join(recommendations.get('suggested_tech_stack', []))}")
    
    print(f"\nMVP Features:")
    for i, feature in enumerate(recommendations.get('mvp_features', []), 1):
        print(f"  {i}. {feature}")