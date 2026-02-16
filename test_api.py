#!/usr/bin/env python3
"""
测试API端点是否正常工作
"""

import requests
import sys
import os

def test_api(base_url):
    """测试API端点"""
    endpoints = [
        ("/", "根端点"),
        ("/health", "健康检查"),
        ("/hello", "Hello端点"),
        ("/stats", "统计信息"),
        ("/docs", "API文档"),
    ]
    
    print(f"测试API端点 (Base URL: {base_url})")
    print("=" * 50)
    
    all_passed = True
    
    for endpoint, description in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {description:15} {url}")
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   响应: {data.get('message', 'OK')}")
                except:
                    print(f"   响应: {response.text[:100]}...")
            else:
                print(f"   错误: {response.text[:100]}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description:15} {url}")
            print(f"   连接错误: {e}")
            all_passed = False
        
        print()
    
    print("=" * 50)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    
    return all_passed

if __name__ == "__main__":
    # 默认测试本地开发服务器
    base_url = "http://localhost:8000"
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    success = test_api(base_url)
    sys.exit(0 if success else 1)