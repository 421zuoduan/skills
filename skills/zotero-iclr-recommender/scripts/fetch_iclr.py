#!/usr/bin/env python3
"""
获取 ICLR 2026 论文列表
"""

import json
import os
import argparse
import requests

def search_iclr_with_tavily(api_key, output_file):
    """使用 Tavily 搜索 ICLR 2026 论文"""
    
    print("正在搜索 ICLR 2026 论文列表...")
    
    # Tavily API
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    
    queries = [
        "ICLR 2026 accepted papers list site:papercopilot.com",
        "ICLR 2026 papers highlights site:paperdigest.org",
        "ICLR 2026 accepted papers -oral -spotlight -poster"
    ]
    
    all_results = []
    
    for query in queries:
        data = {
            "api_key": api_key,
            "query": query,
            "max_results": 10
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            results = response.json().get("results", [])
            all_results.extend(results)
            print(f"  查询 '{query[:40]}...': {len(results)} 结果")
    
    # 去重
    seen = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique_results.append(r)
    
    # 保存搜索结果
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存 {len(unique_results)} 个搜索结果到 {output_file}")
    print("\n参考资源:")
    for r in unique_results[:5]:
        print(f"  - {r['url']}")
    
    return unique_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取 ICLR 2026 论文")
    parser.add_argument("--api-key", required=True, help="Tavily API Key")
    parser.add_argument("--output", default="data/iclr2026_search.json", help="输出文件")
    
    args = parser.parse_args()
    search_iclr_with_tavily(args.api_key, args.output)
