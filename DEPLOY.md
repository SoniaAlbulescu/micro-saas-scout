# 部署指南

## 推荐部署平台：Vercel

Vercel 是部署 Next.js 应用的最佳选择，提供：
- ✅ 完全免费（个人使用）
- ✅ 自动部署（连接GitHub自动更新）
- ✅ 全球CDN加速
- ✅ 自动SSL证书
- ✅ 简单易用

## 部署步骤

### 方法一：通过GitHub部署（推荐）

1. **创建GitHub仓库**
   ```bash
   # 初始化Git仓库
   git init
   git add .
   git commit -m "初始提交"
   
   # 创建GitHub仓库并推送
   # 访问 https://github.com/new 创建新仓库
   git remote add origin https://github.com/你的用户名/micro-saas-scout.git
   git branch -M main
   git push -u origin main
   ```

2. **部署到Vercel**
   - 访问 [vercel.com](https://vercel.com)
   - 使用GitHub账号登录
   - 点击 "New Project"
   - 选择你的 `micro-saas-scout` 仓库
   - 保持默认设置，点击 "Deploy"
   - 等待1-2分钟，获得生产URL（如：`https://micro-saas-scout.vercel.app`）

3. **自动更新**
   - 每次推送到GitHub的main分支，Vercel会自动重新部署
   - 无需手动操作

### 方法二：通过Vercel CLI部署

1. **安装Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登录Vercel**
   ```bash
   vercel login
   ```

3. **部署项目**
   ```bash
   cd micro-saas-scout
   vercel
   ```
   - 按照提示操作
   - 选择默认设置即可

### 方法三：其他平台

#### Netlify
1. 推送到GitHub
2. 访问 [netlify.com](https://netlify.com)
3. 导入仓库，构建命令：`npm run build`，发布目录：`.next`

#### Cloudflare Pages
1. 推送到GitHub
2. 访问 [pages.cloudflare.com](https://pages.cloudflare.com)
3. 选择Next.js模板，自动配置

## 环境变量（后续需要）

当添加后端功能时，可能需要配置环境变量：

```bash
# 在Vercel项目设置中添加
DATABASE_URL=your_database_url
API_KEY=your_api_key
NEXT_PUBLIC_API_URL=https://your-api.com
```

## 自定义域名

1. 在Vercel项目设置中点击 "Domains"
2. 添加你的域名（如：scout.yourdomain.com）
3. 按照提示配置DNS记录
4. 等待SSL证书自动签发

## 监控和维护

### 查看日志
- Vercel仪表板 → 项目 → "Logs"
- 查看部署日志和运行时错误

### 性能监控
- Vercel提供基本的性能监控
- 可集成Google Analytics等工具

### 备份
- 代码备份：GitHub仓库
- 数据备份：当添加数据库后需要定期备份

## 常见问题

### 部署失败
1. 检查 `package.json` 中的依赖是否正确
2. 查看Vercel部署日志中的错误信息
3. 确保Node.js版本兼容（本项目使用Node 18+）

### 访问速度慢
1. Vercel自动使用最近的CDN节点
2. 可配置自定义域名使用国内CDN加速

### 更新后不生效
1. 检查GitHub推送是否成功
2. 查看Vercel部署状态
3. 清除浏览器缓存

## 技术支持

如有问题，可：
1. 查看Vercel文档：https://vercel.com/docs
2. 查看Next.js文档：https://nextjs.org/docs
3. 提交GitHub Issue