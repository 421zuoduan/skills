#!/usr/bin/env python3
"""
使用 Semantic Scholar API 获取论文
"""

import json
import os
import time
import requests

def search_papers(query, max_results=100, output_file=None):
    """搜索论文并获取标题、摘要等"""
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": query,
        "fields": "title,abstract,authors,year,venue",
        "limit": min(max_results, 100),  # 最多100
        "offset": 0
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    results = []
    
    print(f"正在搜索: {query}")
    
    # 添加初始间隔，避免立即被限流
    time.sleep(1)
    
    while len(results) < max_results:
        params["limit"] = min(100, max_results - len(results))
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 429:
                # rate limit，增加等待时间
                print("  Rate limited，等 10 秒...")
                time.sleep(10)
                continue
            
            if response.status_code != 200:
                print(f"  Error: {response.status_code}")
                break
            
            data = response.json()
            papers = data.get("data", [])
            
            if not papers:
                break
            
            for p in papers:
                results.append({
                    "title": p.get("title"),
                    "abstract": p.get("abstract"),
                    "year": p.get("year"),
                    "venue": p.get("venue"),
                    "authors": [a.get("name") for a in p.get("authors", [])[:5]]
                })
            
            print(f"  获取 {len(papers)} 篇，累计 {len(results)} 篇")
            
            # 请求间隔，避免限流
            time.sleep(1.5)
            
            # 检查是否还有更多
            if len(papers) < params["limit"]:
                break
                
            params["offset"] += len(papers)
            
        except Exception as e:
            print(f"  Exception: {e}")
            break
    
    # 保存
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"已保存到 {output_file}")
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="ICLR 2026", help="搜索关键词")
    parser.add_argument("--max", default=50, type=int, help="最大数量")
    parser.add_argument("--output", default="data/semantic_papers.json", help="输出文件")
    args = parser.parse_args()
    
    search_papers(args.query, args.max, args.output)
