import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header'
import Sidebar from '@/components/Sidebar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Micro SaaS Scout - 出海工具需求挖掘系统',
  description: '自动化挖掘出海Micro SaaS工具需求，发现下一个赚钱的小工具',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className={`${inter.className} bg-gray-50 text-gray-900`}>
        <div className="min-h-screen flex flex-col">
          <Header />
          <div className="flex flex-1">
            <Sidebar />
            <main className="flex-1 p-6">
              {children}
            </main>
          </div>
          <footer className="border-t bg-white py-4 text-center text-sm text-gray-500">
            <p>Micro SaaS Scout © 2024 - 自动化需求挖掘系统</p>
            <p className="mt-1">专注于发现出海工具的商业机会</p>
          </footer>
        </div>
      </body>
    </html>
  )
}