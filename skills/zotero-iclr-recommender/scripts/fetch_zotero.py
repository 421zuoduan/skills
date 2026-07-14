#!/usr/bin/env python3
"""
从 Zotero 获取用户论文库
"""

import json
import os
import argparse
import requests

def fetch_zotero_papers(user_id, api_key, output_file):
    """获取 Zotero 用户的所有论文"""
    
    url = f"https://api.zotero.org/users/{user_id}/items"
    headers = {"Zotero-API-Key": api_key}
    
    params = {
        "format": "json",
        "itemType": "journalArticle",
        "limit": 500
    }
    
    all_papers = []
    page = 1
    
    print(f"正在获取 Zotero 论文库 (User: {user_id})...")
    
    while True:
        params["page"] = page - 1
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        papers = response.json()
        if not papers:
            break
            
        all_papers.extend(papers)
        print(f"  第 {page} 页: {len(papers)} 篇, 累计: {len(all_papers)}")
        
        if len(papers) < params["limit"]:
            break
        page += 1
    
    # 提取关键字段
    extracted = []
    for paper in all_papers:
        data = paper.get("data", {})
        extracted.append({
            "title": data.get("title"),
            "authors": [a.get("lastName", "") for a in data.get("creators", [])],
            "year": data.get("date", ""),
            "dateAdded": paper.get("dateAdded", ""),
            "tags": [t.get("tag", "") for t in data.get("tags", [])],
            "url": data.get("url", ""),
            "abstract": data.get("abstractNote", "")
        })
    
    # 保存
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(extracted, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存 {len(extracted)} 篇论文到 {output_file}")
    return extracted

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取 Zotero 论文库")
    parser.add_argument("--user-id", required=True, help="Zotero User ID")
    parser.add_argument("--api-key", required=True, help="Zotero API Key")
    parser.add_argument("--output", default="data/zotero_papers.json", help="输出文件")
    
    args = parser.parse_args()
    fetch_zotero_papers(args.user_id, args.api_key, args.output)
