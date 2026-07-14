#!/usr/bin/env python3
"""
匹配 Zotero 兴趣与 ICLR 2026 论文，并排序输出推荐结果
"""

import json
import os
import argparse
from collections import Counter
import re

def analyze_interest_profile(papers):
    """分析 Zotero 论文库，建立兴趣画像"""
    
    # 统计高频词
    all_titles = " ".join([p.get("title", "") for p in papers if p.get("title")])
    all_tags = []
    for p in papers:
        all_tags.extend(p.get("tags", []))
    
    # 提取关键词（简单实现）
    keywords = []
    for title in [p.get("title", "") for p in papers[:50]]:
        # 提取包含技术词的短语
        patterns = [
            r'\b(LLM|language model|transformer|attention| GPT| BERT| BERT)',
            r'\b(reasoning|chain-of-thought|CoT|self-improvement|reasoning)',
            r'\b(robustness|safety|adversarial|calibration|hallucination)',
            r'\b(multimodal|VLM|vision|Vision-Language)',
            r'\b(efficient|speculative|decoding|KV cache|pruning)',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, title, re.IGNORECASE)
            keywords.extend(matches)
    
    keyword_counts = Counter(keywords)
    top_keywords = [k for k, v in keyword_counts.most_common(20)]
    
    # 最近添加的论文方向
    recent_papers = sorted(papers, key=lambda x: x.get("dateAdded", ""), reverse=True)[:20]
    recent_titles = " ".join([p.get("title", "") for p in recent_papers if p.get("title")])
    
    profile = {
        "top_keywords": top_keywords,
        "recent_focus": recent_titles[:500],
        "total_papers": len(papers),
        "recent_count": len(recent_papers)
    }
    
    return profile

def match_papers(zotero_file, iclr_file, output_file):
    """匹配并排序论文"""
    
    # 加载数据
    with open(zotero_file, "r", encoding="utf-8") as f:
        zotero_papers = json.load(f)
    
    with open(iclr_file, "r", encoding="utf-8") as f:
        iclr_results = json.load(f)
    
    # 分析兴趣画像
    profile = analyze_interest_profile(zotero_papers)
    print("=" * 50)
    print("兴趣画像分析")
    print("=" * 50)
    print(f"论文总数: {profile['total_papers']}")
    print(f"最近阅读: {profile['recent_count']} 篇")
    print(f"核心关键词: {', '.join(profile['top_keywords'][:10])}")
    print()
    
    # 这里需要进一步获取每篇 ICLR 论文的详情
    # 目前先输出搜索结果作为候选
    # 后续可以用大模型进行更精细的匹配
    
    recommendations = []
    for i, result in enumerate(iclr_results[:20]):
        recommendations.append({
            "rank": i + 1,
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "snippet": result.get("content", "")[:300],
            "score": 100 - i * 3,  # 简单评分
            "matched_keywords": [k for k in profile["top_keywords"] if k.lower() in result.get("title", "").lower()]
        })
    
    # 保存结果
    output = {
        "interest_profile": profile,
        "recommendations": recommendations
    }
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"已保存推荐结果到 {output_file}")
    print("\nTop 10 推荐:")
    for r in recommendations[:10]:
        print(f"{r['rank']}. {r['title'][:60]}...")
        print(f"   匹配关键词: {r['matched_keywords']}")
    
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="匹配并排序论文")
    parser.add_argument("--zotero", default="data/zotero_papers.json", help="Zotero 论文文件")
    parser.add_argument("--iclr", default="data/iclr2026_search.json", help="ICLR 搜索结果")
    parser.add_argument("--output", default="data/recommendations.json", help="输出文件")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.zotero):
        print(f"Error: {args.zotero} 不存在，请先运行 fetch_zotero.py")
        exit(1)
    
    if not os.path.exists(args.iclr):
        print(f"Error: {args.iclr} 不存在，请先运行 fetch_iclr.py")
        exit(1)
    
    match_papers(args.zotero, args.iclr, args.output)
