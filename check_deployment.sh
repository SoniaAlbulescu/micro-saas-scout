#!/bin/bash
# 检查Vercel部署状态

echo "🔍 检查Vercel部署状态..."
echo "项目URL: https://micro-saas-scout.vercel.app"
echo "等待部署完成..."

# 等待30秒让Vercel开始部署
sleep 30

echo ""
echo "📊 测试API端点:"

# 测试各个端点
endpoints=("/api/" "/api/health" "/api/hello" "/api/stats" "/api/docs")

for endpoint in "${endpoints[@]}"; do
    url="https://micro-saas-scout.vercel.app${endpoint}"
    echo -n "测试 ${endpoint} ... "
    
    # 使用curl测试，设置超时
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo "✅ 成功 (HTTP $response)"
    elif [ "$response" = "404" ]; then
        echo "❌ 404 Not Found"
    elif [ "$response" = "000" ]; then
        echo "⏳ 超时或无法连接"
    else
        echo "⚠️  HTTP $response"
    fi
    
    sleep 1
done

echo ""
echo "📋 部署状态总结:"
echo "1. 代码已推送到GitHub: ✅"
echo "2. Vercel自动部署: 进行中..."
echo "3. API端点可访问性: 请查看上方测试结果"
echo ""
echo "💡 提示:"
echo "- Vercel部署通常需要1-3分钟"
echo "- 如果仍然显示404，请等待几分钟后重试"
echo "- 可以访问Vercel控制台查看详细部署日志"