import DemandCard from '@/components/DemandCard'
import StatsCard from '@/components/StatsCard'
import { mockDemands, sourceDistribution, pricingDistribution } from '@/lib/data'
import { TrendingUp, Users, DollarSign, Zap, BarChart3, Target } from 'lucide-react'

export default function Home() {
  const topDemands = mockDemands.sort((a, b) => b.scores.overall - a.scores.overall).slice(0, 3)
  
  const stats = [
    {
      title: '总需求数',
      value: '235',
      change: '+12%',
      icon: TrendingUp,
      color: 'blue'
    },
    {
      title: '高潜力机会',
      value: '42',
      change: '+8%',
      icon: Target,
      color: 'green'
    },
    {
      title: '平均月费潜力',
      value: '$24.50',
      change: '+5%',
      icon: DollarSign,
      color: 'purple'
    },
    {
      title: '活跃用户画像',
      value: '8,500+',
      change: '+15%',
      icon: Users,
      color: 'orange'
    }
  ]

  return (
    <div className="space-y-6">
      {/* 欢迎区域 */}
      <div className="rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white">
        <h1 className="mb-2 text-2xl font-bold">欢迎回来，饶阿信！</h1>
        <p className="mb-4 opacity-90">
          今日系统已自动挖掘到 <span className="font-bold">42个</span> 新需求，其中 <span className="font-bold">8个</span> 为高潜力出海工具机会。
        </p>
        <div className="flex gap-4">
          <button className="rounded-lg bg-white px-4 py-2 font-medium text-blue-600 hover:bg-gray-100">
            查看今日报告
          </button>
          <button className="rounded-lg border border-white/30 bg-transparent px-4 py-2 font-medium hover:bg-white/10">
            配置挖掘规则
          </button>
        </div>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <StatsCard key={stat.title} {...stat} />
        ))}
      </div>

      {/* 图表区域 */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-gray-200 bg-white p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">需求增长趋势</h2>
            <select className="rounded-lg border border-gray-300 bg-white px-3 py-1 text-sm">
              <option>最近6个月</option>
              <option>最近12个月</option>
              <option>今年至今</option>
            </select>
          </div>
          <div className="h-64 flex items-center justify-center text-gray-500">
            趋势图表区域（简化版本）
          </div>
        </div>

        <div className="rounded-xl border border-gray-200 bg-white p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">需求来源分布</h2>
            <BarChart3 className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-3">
            {sourceDistribution.map((source) => (
              <div key={source.name} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="h-3 w-3 rounded-full bg-blue-500"></div>
                  <span className="text-sm text-gray-700">{source.name}</span>
                </div>
                <div className="flex items-center gap-4">
                  <div className="h-2 w-32 rounded-full bg-gray-200">
                    <div 
                      className="h-full rounded-full bg-blue-500"
                      style={{ width: `${source.value}%` }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium text-gray-900">{source.value}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 价格分布 */}
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">价格区间分布</h2>
        <div className="grid grid-cols-4 gap-4">
          {pricingDistribution.map((item) => (
            <div key={item.range} className="text-center">
              <div className="mb-2 text-2xl font-bold text-gray-900">{item.count}</div>
              <div className="text-sm text-gray-600">{item.range}</div>
              <div className="mt-2 h-2 rounded-full bg-gray-200">
                <div 
                  className="h-full rounded-full bg-green-500"
                  style={{ width: `${(item.count / 79) * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 今日高潜力需求 */}
      <div>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">今日高潜力需求</h2>
          <button className="text-sm font-medium text-blue-600 hover:text-blue-800">
            查看全部需求 →
          </button>
        </div>
        <div className="space-y-4">
          {topDemands.map((demand) => (
            <DemandCard key={demand.id} demand={demand} />
          ))}
        </div>
      </div>

      {/* 快速行动 */}
      <div className="rounded-xl border border-gray-200 bg-white p-6">
        <h2 className="mb-4 text-lg font-semibold text-gray-900">快速行动</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <button className="flex flex-col items-center justify-center rounded-lg border border-gray-300 p-4 hover:bg-gray-50">
            <Zap className="mb-2 h-8 w-8 text-blue-600" />
            <span className="font-medium">一键生成项目</span>
            <span className="text-sm text-gray-500">基于选定需求</span>
          </button>
          <button className="flex flex-col items-center justify-center rounded-lg border border-gray-300 p-4 hover:bg-gray-50">
            <Target className="mb-2 h-8 w-8 text-green-600" />
            <span className="font-medium">配置监控规则</span>
            <span className="text-sm text-gray-500">自动化挖掘</span>
          </button>
          <button className="flex flex-col items-center justify-center rounded-lg border border-gray-300 p-4 hover:bg-gray-50">
            <DollarSign className="mb-2 h-8 w-8 text-purple-600" />
            <span className="font-medium">定价策略分析</span>
            <span className="text-sm text-gray-500">竞品对比</span>
          </button>
          <button className="flex flex-col items-center justify-center rounded-lg border border-gray-300 p-4 hover:bg-gray-50">
            <Users className="mb-2 h-8 w-8 text-orange-600" />
            <span className="font-medium">用户画像分析</span>
            <span className="text-sm text-gray-500">目标市场</span>
          </button>
        </div>
      </div>
    </div>
  )
}