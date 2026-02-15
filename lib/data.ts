export interface Demand {
  id: string
  title: string
  description: string
  problem: string
  userProfile: {
    role: string
    companySize: string
    techLevel: string
    budget: string
  }
  scenario: string
  painPoints: string[]
  existingSolutions: string[]
  pricingSignals: string[]
  marketSize: {
    searchVolume: number
    competitorUsers: number
    growthRate: number
  }
  technicalFeasibility: {
    complexity: 'low' | 'medium' | 'high'
    devTime: string
    mainTech: string[]
  }
  scores: {
    demandStrength: number
    marketSize: number
    willingnessToPay: number
    technicalFeasibility: number
    passiveIncomeFit: number
    overall: number
  }
  recommendedPricing: string
  mvpFeatures: string[]
  source: string
  discoveredAt: string
  tags: string[]
}

export const mockDemands: Demand[] = [
  {
    id: 'TOOL-001',
    title: '自动将Google Sheets数据同步到Notion',
    description: '用户需要将Google Sheets中的数据自动同步到Notion数据库，避免手动复制粘贴',
    problem: '每周需要花费2-3小时手动同步数据，容易出错且耗时',
    userProfile: {
      role: '项目经理/运营人员',
      companySize: '中小团队(5-20人)',
      techLevel: '非技术用户',
      budget: '$10-30/月'
    },
    scenario: '每周报告同步、跨团队数据共享、实时仪表板更新',
    painPoints: [
      '手动复制粘贴耗时',
      'Zapier太复杂难配置',
      '现有插件功能有限',
      '数据不同步导致决策延迟'
    ],
    existingSolutions: [
      'Zapier（太复杂）',
      '手动复制粘贴',
      '简单的Google Apps Script'
    ],
    pricingSignals: [
      'I\'d pay $20/month for reliable sync',
      'Current solution costs $50 but overkill',
      'Wasting 2 hours weekly on this'
    ],
    marketSize: {
      searchVolume: 1200,
      competitorUsers: 5000,
      growthRate: 25
    },
    technicalFeasibility: {
      complexity: 'medium',
      devTime: '2-3周',
      mainTech: ['Google Sheets API', 'Notion API', 'Node.js']
    },
    scores: {
      demandStrength: 9,
      marketSize: 8,
      willingnessToPay: 8,
      technicalFeasibility: 7,
      passiveIncomeFit: 9,
      overall: 8.5
    },
    recommendedPricing: '$15-25/month',
    mvpFeatures: ['双向同步', '定时任务', '错误处理', '简单配置界面'],
    source: 'Reddit r/SideProject',
    discoveredAt: '2024-02-14',
    tags: ['自动化', '数据同步', '办公效率', '团队协作']
  },
  {
    id: 'TOOL-002',
    title: 'Shopify店铺竞品价格监控',
    description: '自动监控竞争对手Shopify店铺的价格变化，及时调整定价策略',
    problem: '手动检查竞品价格耗时且不及时，错过最佳调价时机',
    userProfile: {
      role: '电商运营/店主',
      companySize: '个人卖家或小团队',
      techLevel: '基础技术能力',
      budget: '$15-40/月'
    },
    scenario: '日常价格监控、促销活动跟踪、市场定价分析',
    painPoints: [
      '每天手动检查多个店铺',
      '价格变化通知不及时',
      '无法跟踪历史价格趋势',
      '错过调价最佳时机'
    ],
    existingSolutions: [
      '手动检查',
      '价格监控服务（太贵）',
      '简单的爬虫脚本'
    ],
    pricingSignals: [
      'Would pay $30/month for accurate monitoring',
      'Losing sales due to price mismatch',
      'Current tools start at $99/month'
    ],
    marketSize: {
      searchVolume: 1800,
      competitorUsers: 8000,
      growthRate: 35
    },
    technicalFeasibility: {
      complexity: 'medium',
      devTime: '3-4周',
      mainTech: ['Shopify API', 'Web Scraping', 'React', 'Node.js']
    },
    scores: {
      demandStrength: 8,
      marketSize: 9,
      willingnessToPay: 9,
      technicalFeasibility: 6,
      passiveIncomeFit: 8,
      overall: 8.2
    },
    recommendedPricing: '$20-35/month',
    mvpFeatures: ['竞品价格监控', '价格变化警报', '历史趋势图表', '简单仪表板'],
    source: 'Shopify社区论坛',
    discoveredAt: '2024-02-13',
    tags: ['电商', '价格监控', '竞争分析', 'Shopify']
  },
  {
    id: 'TOOL-003',
    title: 'AI生成社交媒体帖子配图',
    description: '根据社交媒体帖子内容自动生成匹配的配图，提高内容吸引力',
    problem: '为每个帖子找配图耗时，图片质量参差不齐，风格不统一',
    userProfile: {
      role: '社交媒体经理/内容创作者',
      companySize: '个人或小团队',
      techLevel: '非技术用户',
      budget: '$12-25/月'
    },
    scenario: '日常社交媒体发布、内容营销、品牌一致性维护',
    painPoints: [
      '找图耗时（每帖15-30分钟）',
      '图片版权问题',
      '风格不一致',
      '图片与内容不匹配'
    ],
    existingSolutions: [
      'Canva（手动操作）',
      'Unsplash搜索',
      'AI图像生成工具（需手动调整）'
    ],
    pricingSignals: [
      'Spend 10+ hours monthly on images',
      'Would pay $20 for consistent branding',
      'Current tools lack automation'
    ],
    marketSize: {
      searchVolume: 2500,
      competitorUsers: 12000,
      growthRate: 40
    },
    technicalFeasibility: {
      complexity: 'high',
      devTime: '4-6周',
      mainTech: ['OpenAI API', 'Stable Diffusion', 'React', 'Node.js']
    },
    scores: {
      demandStrength: 9,
      marketSize: 9,
      willingnessToPay: 7,
      technicalFeasibility: 5,
      passiveIncomeFit: 8,
      overall: 7.8
    },
    recommendedPricing: '$15-30/month',
    mvpFeatures: ['文本到图像生成', '品牌风格学习', '批量处理', '简单编辑器'],
    source: 'Twitter营销社区',
    discoveredAt: '2024-02-12',
    tags: ['AI', '社交媒体', '内容创作', '自动化']
  },
  {
    id: 'TOOL-004',
    title: 'Chrome扩展：网页内容一键保存到Notion',
    description: '浏览网页时一键将内容保存到指定的Notion页面或数据库',
    problem: '收藏了大量网页但难以整理，信息分散在不同地方',
    userProfile: {
      role: '研究人员/学生/知识工作者',
      companySize: '个人使用',
      techLevel: '普通用户',
      budget: '$5-15/月'
    },
    scenario: '研究资料收集、内容灵感保存、知识管理',
    painPoints: [
      '书签难以管理',
      '内容分散在不同工具',
      '无法添加笔记和标签',
      '搜索困难'
    ],
    existingSolutions: [
      '浏览器书签',
      'Pocket/Instapaper',
      '手动复制到Notion'
    ],
    pricingSignals: [
      'Would pay $10 for seamless saving',
      'Currently using free but limited tools',
      'Saves 1+ hour weekly'
    ],
    marketSize: {
      searchVolume: 3200,
      competitorUsers: 15000,
      growthRate: 30
    },
    technicalFeasibility: {
      complexity: 'low',
      devTime: '1-2周',
      mainTech: ['Chrome Extension API', 'Notion API', 'JavaScript']
    },
    scores: {
      demandStrength: 8,
      marketSize: 9,
      willingnessToPay: 6,
      technicalFeasibility: 9,
      passiveIncomeFit: 9,
      overall: 8.4
    },
    recommendedPricing: '$8-12/month',
    mvpFeatures: ['一键保存', '标签分类', '笔记添加', '搜索功能'],
    source: 'Chrome Web Store评论',
    discoveredAt: '2024-02-11',
    tags: ['浏览器扩展', '知识管理', '生产力', 'Notion']
  },
  {
    id: 'TOOL-005',
    title: 'Slack机器人：自动生成会议纪要',
    description: '在Slack会议频道中自动记录讨论要点并生成会议纪要',
    problem: '会议记录耗时且容易遗漏重要信息，后续难以查找',
    userProfile: {
      role: '团队负责人/项目经理',
      companySize: '中小团队(10-50人)',
      techLevel: '非技术用户',
      budget: '$20-50/月（团队）'
    },
    scenario: '团队日常会议、项目讨论、决策记录',
    painPoints: [
      '专人记录耗时',
      '信息遗漏',
      '后续查找困难',
      '行动项跟踪缺失'
    ],
    existingSolutions: [
      '手动记录',
      '录音转文字服务',
      '专门的会议工具'
    ],
    pricingSignals: [
      'Team would pay $40/month',
      'Saves 5+ hours weekly',
      'Better than $99/month alternatives'
    ],
    marketSize: {
      searchVolume: 1500,
      competitorUsers: 6000,
      growthRate: 28
    },
    technicalFeasibility: {
      complexity: 'medium',
      devTime: '3-4周',
      mainTech: ['Slack API', 'OpenAI API', 'Node.js']
    },
    scores: {
      demandStrength: 7,
      marketSize: 8,
      willingnessToPay: 8,
      technicalFeasibility: 7,
      passiveIncomeFit: 8,
      overall: 7.8
    },
    recommendedPricing: '$30-45/month（团队）',
    mvpFeatures: ['自动记录', '要点提取', '行动项识别', '搜索功能'],
    source: 'Slack社区',
    discoveredAt: '2024-02-10',
    tags: ['Slack', '会议效率', '团队协作', 'AI']
  }
]

export const trendsData = [
  { month: '1月', demandCount: 120, highPotential: 15 },
  { month: '2月', demandCount: 145, highPotential: 22 },
  { month: '3月', demandCount: 168, highPotential: 28 },
  { month: '4月', demandCount: 192, highPotential: 35 },
  { month: '5月', demandCount: 210, highPotential: 42 },
  { month: '6月', demandCount: 235, highPotential: 48 },
]

export const sourceDistribution = [
  { name: 'Reddit', value: 35 },
  { name: 'Product Hunt', value: 25 },
  { name: 'Chrome Store', value: 20 },
  { name: 'Twitter', value: 15 },
  { name: '其他', value: 5 },
]

export const pricingDistribution = [
  { range: '$5-10', count: 22 },
  { range: '$10-20', count: 31 },
  { range: '$20-50', count: 18 },
  { range: '$50+', count: 8 },
]