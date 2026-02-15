import { Demand } from '@/lib/data'
import { Star, Users, DollarSign, Zap, TrendingUp, Clock, ExternalLink, Tag } from 'lucide-react'

interface DemandCardProps {
  demand: Demand
}

export default function DemandCard({ demand }: DemandCardProps) {
  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 8.5) return 'bg-gradient-to-r from-green-500 to-emerald-600'
    if (score >= 7.5) return 'bg-gradient-to-r from-blue-500 to-cyan-600'
    if (score >= 6.5) return 'bg-gradient-to-r from-yellow-500 to-orange-500'
    return 'bg-gradient-to-r from-gray-400 to-gray-600'
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-all hover:shadow-md">
      <div className="mb-4 flex items-start justify-between">
        <div className="flex-1">
          <div className="mb-2 flex items-center gap-2">
            <span className="rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-800">
              {demand.id}
            </span>
            <span className="text-xs text-gray-500">
              <Clock className="mr-1 inline h-3 w-3" />
              {demand.discoveredAt}
            </span>
          </div>
          <h3 className="mb-2 text-lg font-semibold text-gray-900">{demand.title}</h3>
          <p className="mb-3 text-sm text-gray-600">{demand.description}</p>
          
          <div className="mb-4 flex flex-wrap gap-2">
            {demand.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-3 py-1 text-xs text-gray-700"
              >
                <Tag className="h-3 w-3" />
                {tag}
              </span>
            ))}
          </div>
        </div>
        
        <div className="ml-4">
          <div className={`rounded-lg px-3 py-2 text-center text-white ${getScoreColor(demand.scores.overall)}`}>
            <div className="text-2xl font-bold">{demand.scores.overall.toFixed(1)}</div>
            <div className="text-xs opacity-90">综合评分</div>
          </div>
        </div>
      </div>

      <div className="mb-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="rounded-lg bg-gray-50 p-3">
          <div className="mb-1 flex items-center gap-1 text-sm text-gray-600">
            <Star className="h-4 w-4" />
            需求强度
          </div>
          <div className="text-lg font-semibold">{demand.scores.demandStrength}/10</div>
        </div>
        <div className="rounded-lg bg-gray-50 p-3">
          <div className="mb-1 flex items-center gap-1 text-sm text-gray-600">
            <Users className="h-4 w-4" />
            市场规模
          </div>
          <div className="text-lg font-semibold">{demand.scores.marketSize}/10</div>
        </div>
        <div className="rounded-lg bg-gray-50 p-3">
          <div className="mb-1 flex items-center gap-1 text-sm text-gray-600">
            <DollarSign className="h-4 w-4" />
            付费意愿
          </div>
          <div className="text-lg font-semibold">{demand.scores.willingnessToPay}/10</div>
        </div>
        <div className="rounded-lg bg-gray-50 p-3">
          <div className="mb-1 flex items-center gap-1 text-sm text-gray-600">
            <Zap className="h-4 w-4" />
            技术可行
          </div>
          <div className="text-lg font-semibold">{demand.scores.technicalFeasibility}/10</div>
        </div>
      </div>

      <div className="mb-4 grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <h4 className="mb-2 text-sm font-semibold text-gray-700">用户画像</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">角色:</span>
              <span className="font-medium">{demand.userProfile.role}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">团队规模:</span>
              <span className="font-medium">{demand.userProfile.companySize}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">技术能力:</span>
              <span className="font-medium">{demand.userProfile.techLevel}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">预算范围:</span>
              <span className="font-medium text-green-600">{demand.userProfile.budget}</span>
            </div>
          </div>
        </div>
        
        <div>
          <h4 className="mb-2 text-sm font-semibold text-gray-700">技术评估</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">开发复杂度:</span>
              <span className={`rounded-full px-2 py-1 text-xs font-medium ${getComplexityColor(demand.technicalFeasibility.complexity)}`}>
                {demand.technicalFeasibility.complexity === 'low' ? '低' : 
                 demand.technicalFeasibility.complexity === 'medium' ? '中' : '高'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">开发时间:</span>
              <span className="font-medium">{demand.technicalFeasibility.devTime}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">主要技术:</span>
              <span className="font-medium">{demand.technicalFeasibility.mainTech.join(', ')}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <h4 className="mb-2 text-sm font-semibold text-gray-700">市场数据</h4>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div className="rounded-lg bg-blue-50 p-3">
            <div className="text-gray-600">月搜索量</div>
            <div className="text-lg font-semibold">{demand.marketSize.searchVolume.toLocaleString()}</div>
          </div>
          <div className="rounded-lg bg-purple-50 p-3">
            <div className="text-gray-600">竞品用户</div>
            <div className="text-lg font-semibold">{demand.marketSize.competitorUsers.toLocaleString()}+</div>
          </div>
          <div className="rounded-lg bg-green-50 p-3">
            <div className="text-gray-600">年增长率</div>
            <div className="text-lg font-semibold">{demand.marketSize.growthRate}%</div>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between border-t pt-4">
        <div>
          <div className="text-sm text-gray-600">推荐定价</div>
          <div className="text-lg font-bold text-green-600">{demand.recommendedPricing}</div>
        </div>
        <div className="flex gap-2">
          <button className="rounded-lg border border-blue-600 bg-white px-4 py-2 text-sm font-medium text-blue-600 hover:bg-blue-50">
            查看详情
          </button>
          <button className="rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-2 text-sm font-medium text-white hover:opacity-90">
            生成项目框架
          </button>
        </div>
      </div>
    </div>
  )
}