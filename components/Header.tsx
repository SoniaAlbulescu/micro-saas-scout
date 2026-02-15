import { Search, Bell, User, Sparkles } from 'lucide-react'

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 p-2">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Micro SaaS Scout</h1>
              <p className="text-xs text-gray-500">出海工具需求挖掘系统</p>
            </div>
          </div>
          
          <nav className="ml-10 hidden md:flex items-center gap-6">
            <a href="/" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              仪表板
            </a>
            <a href="/discover" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              需求发现
            </a>
            <a href="/trends" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              趋势分析
            </a>
            <a href="/competitors" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              竞品监控
            </a>
            <a href="/pricing" className="text-sm font-medium text-gray-700 hover:text-blue-600">
              定价策略
            </a>
          </nav>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative hidden md:block">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="search"
              placeholder="搜索需求、工具、关键词..."
              className="block w-64 rounded-lg border border-gray-300 bg-gray-50 py-2 pl-10 pr-3 text-sm placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <button className="relative rounded-lg p-2 text-gray-600 hover:bg-gray-100">
            <Bell className="h-5 w-5" />
            <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-xs text-white">
              3
            </span>
          </button>

          <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white px-3 py-2">
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500"></div>
            <div className="hidden sm:block">
              <p className="text-sm font-medium">饶阿信</p>
              <p className="text-xs text-gray-500">出海工具探索者</p>
            </div>
            <User className="h-5 w-5 text-gray-400" />
          </div>
        </div>
      </div>
    </header>
  )
}