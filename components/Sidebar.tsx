import { 
  Home, 
  TrendingUp, 
  DollarSign, 
  Users, 
  BarChart3, 
  Target, 
  Zap, 
  Clock,
  Filter,
  Star
} from 'lucide-react'

const filters = [
  { icon: Star, label: '高评分需求', count: 24, color: 'text-yellow-500' },
  { icon: DollarSign, label: '高付费意愿', count: 18, color: 'text-green-500' },
  { icon: Zap, label: '技术可行', count: 32, color: 'text-blue-500' },
  { icon: Users, label: '团队工具', count: 15, color: 'text-purple-500' },
  { icon: Clock, label: '近期热门', count: 12, color: 'text-orange-500' },
]

const toolTypes = [
  { name: '浏览器扩展', count: 28 },
  { name: 'API服务', count: 19 },
  { name: 'Chrome插件', count: 24 },
  { name: 'Shopify应用', count: 16 },
  { name: 'Slack机器人', count: 11 },
  { name: 'CLI工具', count: 9 },
  { name: '微信小程序', count: 7 },
  { name: '移动应用', count: 5 },
]

const priceRanges = [
  { range: '$5-10/月', count: 22 },
  { range: '$10-20/月', count: 31 },
  { range: '$20-50/月', count: 18 },
  { range: '$50+/月', count: 8 },
]

export default function Sidebar() {
  return (
    <aside className="hidden w-64 border-r bg-white lg:block">
      <div className="sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto p-6">
        <div className="mb-8">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-gray-500">
            <Filter className="h-4 w-4" />
            快速筛选
          </h2>
          <div className="space-y-2">
            {filters.map((filter) => (
              <button
                key={filter.label}
                className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm hover:bg-gray-50"
              >
                <div className="flex items-center gap-3">
                  <filter.icon className={`h-4 w-4 ${filter.color}`} />
                  <span className="text-gray-700">{filter.label}</span>
                </div>
                <span className="rounded-full bg-gray-100 px-2 py-1 text-xs font-medium">
                  {filter.count}
                </span>
              </button>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-gray-500">
            <Target className="h-4 w-4" />
            工具类型
          </h2>
          <div className="space-y-2">
            {toolTypes.map((type) => (
              <button
                key={type.name}
                className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm hover:bg-gray-50"
              >
                <span className="text-gray-700">{type.name}</span>
                <span className="text-xs text-gray-500">{type.count}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="mb-8">
          <h2 className="mb-4 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-gray-500">
            <DollarSign className="h-4 w-4" />
            价格区间
          </h2>
          <div className="space-y-2">
            {priceRanges.map((range) => (
              <button
                key={range.range}
                className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm hover:bg-gray-50"
              >
                <span className="text-gray-700">{range.range}</span>
                <span className="text-xs text-gray-500">{range.count}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-lg bg-gradient-to-br from-blue-50 to-purple-50 p-4">
          <h3 className="mb-2 text-sm font-semibold text-gray-900">今日统计</h3>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-gray-600">新发现需求</p>
              <p className="text-lg font-bold text-gray-900">42个</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">高潜力机会</p>
              <p className="text-lg font-bold text-gray-900">8个</p>
            </div>
            <div>
              <p className="text-xs text-gray-600">平均月费潜力</p>
              <p className="text-lg font-bold text-gray-900">$24.50</p>
            </div>
          </div>
          <button className="mt-4 w-full rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 py-2 text-sm font-medium text-white hover:opacity-90">
            生成今日报告
          </button>
        </div>
      </div>
    </aside>
  )
}