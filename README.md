# Micro SaaS Scout - 出海工具需求挖掘系统

专为饶阿信打造的自动化需求挖掘平台。

## 🎯 功能特点

### 前端（已完成）
- 📊 仪表板界面 - 关键指标和趋势图表
- 🃏 需求卡片 - 详细的需求信息展示
- 🔍 智能筛选 - 按评分、类型、价格筛选
- 📈 数据可视化 - 趋势和分布图表
- 📱 响应式设计 - 适配各种设备

### 后端（新增）
- 🕷️ **数据采集** - 自动从HackerNews等平台抓取需求
- 🧠 **智能分析** - NLP分析需求并自动评分
- 💾 **数据库存储** - PostgreSQL存储所有数据
- 🔄 **数据管道** - 完整的爬取-分析-存储流程
- 📡 **RESTful API** - 提供完整的数据接口

## 🚀 技术栈

### 前端
- Next.js 14 + TypeScript
- Tailwind CSS
- React + 现代Hooks

### 后端
- Python + FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy ORM
- BeautifulSoup4 + Requests (爬虫)
- NLTK (自然语言处理)

### 部署
- Vercel (前端 + Serverless函数)
- Supabase (数据库)

## 📁 项目结构

```
micro-saas-scout/
├── api/                    # Vercel云函数 (FastAPI)
│   ├── demands/           # 需求管理API
│   ├── crawl/             # 爬取任务API
│   └── index.py           # 主API入口
├── backend/               # 后端核心逻辑
│   ├── database/          # 数据库模型和连接
│   ├── crawlers/          # 数据采集器
│   ├── analysis/          # 需求分析引擎
│   └── utils/             # 工具函数
├── app/                   # Next.js前端
├── components/            # React组件
├── lib/                   # 前端工具函数
└── public/                # 静态资源
```

## 🔧 快速开始

### 1. 环境变量配置
在Vercel项目中设置：
- `DATABASE_URL`: Supabase PostgreSQL连接字符串

### 2. API端点
```
GET    /api/health         # 健康检查
GET    /api/demands        # 获取需求列表
POST   /api/demands        # 创建新需求
GET    /api/demands/stats  # 需求统计
POST   /api/crawl/start    # 启动数据爬取
GET    /api/crawl/status   # 查看爬取状态
```

### 3. 数据管道流程
```
1. 爬取HackerNews帖子
2. 提取潜在工具需求
3. NLP分析需求内容
4. 自动评分和分类
5. 保存到数据库
6. 通过API提供给前端
```

## 🎯 核心功能

### 自动化需求挖掘
- 从HackerNews "Show HN" 和 "Ask HN" 抓取
- 识别工具需求和问题讨论
- 提取关键信息和上下文

### 智能分析系统
- **需求强度评分** - 问题紧迫性
- **市场规模评估** - 潜在用户数量
- **付费意愿分析** - 价格敏感度
- **技术可行性** - 开发复杂度
- **被动收入适配度** - 商业模式匹配

### 数据库设计
- `demands` 表 - 存储所有挖掘到的需求
- `sources` 表 - 数据源配置和状态
- `analysis_results` 表 - 分析结果

## 🚀 部署

### 前端部署（Vercel）
1. 推送到GitHub仓库
2. Vercel自动检测并部署
3. 配置环境变量

### 后端部署（Vercel Serverless）
1. API代码在 `api/` 目录
2. Vercel自动识别Python函数
3. 自动安装依赖并部署

### 数据库（Supabase）
1. 免费PostgreSQL数据库
2. 自动备份和监控
3. 可视化数据管理

## 📈 下一步开发

### 短期计划
1. 添加更多数据源（Reddit, Product Hunt）
2. 优化分析算法准确度
3. 实现定时自动爬取
4. 添加用户反馈系统

### 长期计划
1. 机器学习模型训练
2. 多语言支持
3. 高级分析报告
4. 商业化功能

## 🔒 安全考虑

- 数据库密码通过环境变量管理
- API请求限流和认证
- 爬虫遵守robots.txt
- 数据隐私保护

## 📞 支持

如有问题或建议，请提交GitHub Issue或联系维护者。