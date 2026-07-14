#!/usr/bin/env python3
"""
论文下载脚本 v4 - Academic Paper Downloader
=============================================
全自动 SOP Pipeline:
  1. Semantic Scholar REST API 精准搜索（获取会议/期刊 + OpenAccessPdf）
  2. Semantic Scholar 模糊搜索（关键词 + 摘要/作者验证）
  3. 级联下载: OpenAccessPdf -> OpenReview -> PMLR -> arXiv
  4. pypdf 首页校验（防幻觉）
  5. 规范重命名: [会议 年份] 或 [arXiv_ID]

使用方法：
    python3 paper_downloader.py "论文标题1" "论文标题2"
    python3 paper_downloader.py --file titles.txt
    python3 paper_downloader.py --file titles.txt --output /path/to/output
"""

import os
import sys
import re
import json
import argparse
import time
import requests
from pathlib import Path

# ========== 依赖检查 ==========
MISSING = []
try:
    import arxiv
except ImportError:
    MISSING.append("arxiv")
try:
    from pypdf import PdfReader
except ImportError:
    MISSING.append("pypdf")
if MISSING:
    print(f"缺少依赖: {', '.join(MISSING)}")
    print(f"请运行: pip install {' '.join(MISSING)}")
    sys.exit(1)

# ========== 全局配置 ==========
OUTPUT_DIR = Path("./downloaded_papers")
SS_API = "https://api.semanticscholar.org/graph/v1"
SS_FIELDS = "title,venue,year,authors,externalIds,openAccessPdf,abstract"
OR_API_V2 = "https://api2.openreview.net/notes/search"
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
arxiv_client = arxiv.Client()

# SS API 限速管理
_last_ss_call = 0.0
SS_MIN_INTERVAL = 1.2  # 秒


def _ss_throttle():
    """Semantic Scholar API 限速控制"""
    global _last_ss_call
    elapsed = time.time() - _last_ss_call
    if elapsed < SS_MIN_INTERVAL:
        time.sleep(SS_MIN_INTERVAL - elapsed)
    _last_ss_call = time.time()


# ========== 工具函数 ==========

def clean_filename(name: str) -> str:
    """去除 Windows/Linux 非法路径字符"""
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def extract_keywords(title: str) -> list:
    """从标题提取核心关键词"""
    cleaned = re.sub(r'[:\-–—,;\.()]', ' ', title)
    stopwords = {
        'the', 'and', 'for', 'with', 'from', 'using', 'via', 'based',
        'against', 'towards', 'toward', 'into', 'over', 'under', 'between',
        'about', 'that', 'this', 'then', 'than', 'also', 'more', 'most',
        'very', 'each', 'every', 'both', 'some', 'such', 'only',
    }
    words = cleaned.split()
    return [w for w in words if len(w) >= 4 and w.lower() not in stopwords]


def title_match_score(query_title: str, candidate_title: str) -> float:
    """计算标题关键词匹配度 (0~1)"""
    kw_q = set(w.lower() for w in extract_keywords(query_title))
    kw_c = set(w.lower() for w in extract_keywords(candidate_title))
    if not kw_q:
        return 0.0
    return len(kw_q & kw_c) / len(kw_q)


VENUE_MAP = {
    "neurips": "NeurIPS", "nips": "NeurIPS",
    "neural information processing": "NeurIPS",
    "iclr": "ICLR", "international conference on learning representations": "ICLR",
    "icml": "ICML", "international conference on machine learning": "ICML",
    "cvpr": "CVPR", "computer vision and pattern recognition": "CVPR",
    "iccv": "ICCV", "international conference on computer vision": "ICCV",
    "eccv": "ECCV", "european conference on computer vision": "ECCV",
    "acl": "ACL", "association for computational linguistics": "ACL",
    "emnlp": "EMNLP", "empirical methods in natural language": "EMNLP",
    "naacl": "NAACL", "coling": "COLING",
    "aaai": "AAAI", "ijcai": "IJCAI",
    "kdd": "KDD", "www": "WWW", "sigir": "SIGIR",
    "corl": "CoRL", "icra": "ICRA", "iros": "IROS",
    "uai": "UAI", "aistats": "AISTATS", "colt": "COLT",
    "l4dc": "L4DC", "learning for dynamics": "L4DC",
    "iccv": "ICCV", "wacv": "WACV",
    "interspeech": "Interspeech", "icassp": "ICASSP",
}


def normalize_venue(venue: str) -> str:
    """标准化会议/期刊名称，返回 None 表示未知"""
    if not venue:
        return None
    vl = venue.strip().lower()
    if "arxiv" in vl:
        return None
    for key, val in VENUE_MAP.items():
        if key in vl:
            return val
    # 如果字符串很短且是大写，可能本身就是缩写
    if len(venue.strip()) <= 10 and venue.strip().isupper():
        return venue.strip()
    return venue.strip()  # 返回原始值


def _parse_ss_paper(paper: dict) -> dict:
    """解析 Semantic Scholar API 返回的 paper 对象"""
    ext = paper.get("externalIds") or {}
    oap = paper.get("openAccessPdf") or {}
    venue_raw = paper.get("venue", "")
    year = paper.get("year")
    venue = normalize_venue(venue_raw)
    dblp_id = ext.get("DBLP", "")

    return {
        "title": paper.get("title", ""),
        "venue": venue,
        "year": year,
        "authors": [a.get("name", "") for a in (paper.get("authors") or [])[:5]],
        "arxiv_id": ext.get("ArXiv"),
        "doi": ext.get("DOI"),
        "dblp_id": dblp_id,
        "oa_pdf": oap.get("url") if isinstance(oap, dict) and oap.get("url") else None,
        "abstract": paper.get("abstract", "") or "",
    }


# ================================================================
#  第一步: 精准搜索 (Semantic Scholar REST API)
# ================================================================

def step1_exact_search(title: str) -> dict:
    """Semantic Scholar 精准搜索"""
    _ss_throttle()
    try:
        resp = requests.get(
            f"{SS_API}/paper/search",
            params={"query": title, "limit": 5, "fields": SS_FIELDS},
            timeout=15,
        )
        if resp.status_code == 429:
            print("    SS 限速，等待 5 秒重试...")
            time.sleep(5)
            _ss_throttle()
            resp = requests.get(
                f"{SS_API}/paper/search",
                params={"query": title, "limit": 5, "fields": SS_FIELDS},
                timeout=15,
            )
        if resp.status_code != 200:
            print(f"    SS API HTTP {resp.status_code}")
            return None

        data = resp.json().get("data", [])
        if not data:
            return None

        # 选最佳匹配
        best, best_score = None, 0
        for p in data:
            score = title_match_score(title, p.get("title", ""))
            if score > best_score:
                best, best_score = p, score

        if best and best_score >= 0.6:
            info = _parse_ss_paper(best)
            info["match_score"] = best_score
            info["source"] = "SS-exact"
            return info

    except requests.exceptions.Timeout:
        print("    SS API 超时")
    except Exception as e:
        print(f"    SS 精准搜索异常: {e}")
    return None


# ================================================================
#  第二步: 模糊搜索 + 二次验证
# ================================================================

def step2_fuzzy_search(title: str) -> dict:
    """Semantic Scholar 模糊搜索 + 摘要/作者验证"""
    keywords = extract_keywords(title)
    if not keywords:
        return None
    query = " ".join(keywords[:6])
    print(f"    模糊关键词: {query}")

    _ss_throttle()
    try:
        resp = requests.get(
            f"{SS_API}/paper/search",
            params={"query": query, "limit": 10, "fields": SS_FIELDS},
            timeout=15,
        )
        if resp.status_code == 429:
            print("    SS 限速，等待 5 秒重试...")
            time.sleep(5)
            _ss_throttle()
            resp = requests.get(
                f"{SS_API}/paper/search",
                params={"query": query, "limit": 10, "fields": SS_FIELDS},
                timeout=15,
            )
        if resp.status_code != 200:
            return None

        data = resp.json().get("data", [])
        for p in data:
            score = title_match_score(title, p.get("title", ""))
            if score < 0.5:
                continue
            # 二次验证: 检查摘要是否包含查询关键词
            abstract = (p.get("abstract") or "").lower()
            kw_hits = sum(1 for kw in keywords[:4] if kw.lower() in abstract)
            if score >= 0.7 or kw_hits >= 2:
                info = _parse_ss_paper(p)
                info["match_score"] = score
                info["source"] = "SS-fuzzy"
                return info

    except Exception as e:
        print(f"    SS 模糊搜索异常: {e}")
    return None


def step2b_arxiv_search(title: str) -> dict:
    """arXiv 搜索兜底"""
    try:
        search = arxiv.Search(query=f'"{title}"', max_results=3)
        results = list(arxiv_client.results(search))
        if not results:
            keywords = extract_keywords(title)
            if keywords:
                search = arxiv.Search(query=" ".join(keywords[:6]), max_results=5)
                results = list(arxiv_client.results(search))

        for paper in results:
            score = title_match_score(title, paper.title)
            if score >= 0.5:
                aid = paper.entry_id.split("/")[-1]
                return {
                    "title": paper.title,
                    "venue": None,
                    "year": paper.published.year if paper.published else None,
                    "authors": [a.name for a in paper.authors[:5]],
                    "arxiv_id": aid,
                    "doi": None,
                    "dblp_id": "",
                    "oa_pdf": paper.pdf_url,
                    "abstract": paper.summary or "",
                    "match_score": score,
                    "source": "arXiv",
                }
    except Exception as e:
        print(f"    arXiv 搜索异常: {e}")
    return None


# ================================================================
#  第三步: 级联下载
# ================================================================

def _download_to(url: str, save_path: str) -> bool:
    """下载 URL 到本地文件"""
    try:
        resp = requests.get(url, timeout=120, headers=HTTP_HEADERS)
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(save_path, "wb") as f:
                f.write(resp.content)
            return True
        else:
            print(f"    HTTP {resp.status_code}, size={len(resp.content) if resp.status_code==200 else 'N/A'}")
    except Exception as e:
        print(f"    下载异常: {e}")
    return False


def _try_openreview(title: str) -> str:
    """OpenReview API v2 搜索，返回 PDF URL"""
    try:
        resp = requests.get(OR_API_V2, params={"query": title, "limit": 5}, timeout=15)
        if resp.status_code != 200:
            return None
        notes = resp.json().get("notes", [])
        for note in notes:
            content = note.get("content", {})
            note_title = content.get("title", {})
            if isinstance(note_title, dict):
                note_title = note_title.get("value", "")
            if title_match_score(title, str(note_title)) >= 0.6:
                forum_id = note.get("id")
                if forum_id:
                    return f"https://openreview.net/pdf?id={forum_id}"
    except Exception as e:
        print(f"    OpenReview 异常: {e}")
    return None


def _try_pmlr(dblp_id: str, title: str = "") -> str:
    """根据 DBLP ID 或论文标题搜索 PMLR PDF"""
    # 通过 DBLP 搜索 API 获取 URL（用 params 自动编码）
    if title:
        try:
            resp = requests.get(
                "https://dblp.org/search/publ/api",
                params={"q": title, "format": "json", "h": "3"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                hits = data.get("result", {}).get("hits", {}).get("hit", [])
                # hits 可能是 dict（单个结果）而非 list
                if isinstance(hits, dict):
                    hits = [hits]
                print(f"    DBLP 找到 {len(hits)} 条结果")
                for hit in hits:
                    info = hit.get("info", {})
                    ee = info.get("ee")
                    if ee:
                        urls = ee if isinstance(ee, list) else [ee]
                        for url in urls:
                            url = str(url)
                            if "mlr.press" in url:
                                if url.endswith(".html"):
                                    base = url.rsplit("/", 1)[-1].replace(".html", "")
                                    return url.replace(".html", f"/{base}.pdf")
                                elif url.endswith(".pdf"):
                                    return url
        except Exception as e:
            print(f"    DBLP 搜索异常: {e}")
    return None


def step3_cascade_download(info: dict, title: str, temp_path: str) -> bool:
    """级联下载: OpenAccessPdf -> OpenReview -> PMLR -> arXiv"""

    # 优先级 1: Semantic Scholar OpenAccessPdf
    if info.get("oa_pdf"):
        print(f"    [优先级1] OpenAccessPdf: {info['oa_pdf'][:60]}...")
        if _download_to(info["oa_pdf"], temp_path):
            return True
        print(f"    OpenAccessPdf 下载失败，尝试下一个...")

    # 优先级 2: OpenReview
    print(f"    [优先级2] 搜索 OpenReview...")
    or_url = _try_openreview(title)
    if or_url:
        print(f"    找到: {or_url}")
        if _download_to(or_url, temp_path):
            return True
        print(f"    OpenReview 下载失败，尝试下一个...")

    # 优先级 2.5: PMLR (通过 DBLP 搜索 - 始终尝试)
    print(f"    [优先级2.5] 尝试 PMLR/DBLP...")
    pmlr_url = _try_pmlr(info.get("dblp_id", ""), title)
    if pmlr_url:
        print(f"    找到 PMLR: {pmlr_url}")
        if _download_to(pmlr_url, temp_path):
            return True

    # 优先级 3: arXiv
    arxiv_id = info.get("arxiv_id")
    if arxiv_id:
        clean_id = re.sub(r"v\d+$", "", arxiv_id)
        url = f"https://arxiv.org/pdf/{clean_id}.pdf"
        print(f"    [优先级3] arXiv: {url}")
        if _download_to(url, temp_path):
            return True

    return False


# ================================================================
#  第三步续: pypdf 首页校验
# ================================================================

def step3_validate(pdf_path: str, original_title: str) -> bool:
    """pypdf 读取第一页，检查标题核心词汇是否存在"""
    try:
        reader = PdfReader(pdf_path)
        if len(reader.pages) == 0:
            print("    PDF 无页面")
            return False
        text = reader.pages[0].extract_text().lower()

        keywords = extract_keywords(original_title)
        important = [w.lower() for w in keywords if len(w) >= 5]
        if not important:
            important = [w.lower() for w in keywords]
        if not important:
            return False

        hits = sum(1 for w in important if w in text)
        ratio = hits / len(important) if important else 0
        print(f"    首页校验: {hits}/{len(important)} 关键词命中 ({ratio:.0%})")
        return ratio >= 0.4
    except Exception as e:
        print(f"    PDF 校验异常: {e}")
        return False


# ================================================================
#  第四步: 规范重命名
# ================================================================

def step4_rename(info: dict) -> str:
    """生成规范文件名: [会议 年份] 或 [arXiv_ID]"""
    venue = info.get("venue")
    year = info.get("year")
    arxiv_id = info.get("arxiv_id")
    title = info.get("title", "Unknown")

    if venue:
        prefix = f"[{venue} {year}]" if year else f"[{venue}]"
    elif arxiv_id:
        clean_id = re.sub(r"v\d+$", "", arxiv_id)
        prefix = f"[arXiv_{clean_id}]"
    else:
        prefix = f"[{year}]" if year else "[Unknown]"

    filename = f"{prefix} {title}.pdf"
    return clean_filename(filename)


# ================================================================
#  主 Pipeline
# ================================================================

def process_paper(title: str, index: int, total: int) -> dict:
    """单篇论文完整处理流程"""
    print(f"\n{'='*60}")
    print(f"[{index}/{total}] {title}")
    print(f"{'='*60}")

    result = {"title": title, "status": "failed", "filename": None, "reason": None}
    info = None

    # ===== 第一步: 精准搜索 =====
    print(f"  [Step 1] Semantic Scholar 精准搜索...")
    info = step1_exact_search(title)
    if info:
        print(f"    -> 命中! 匹配度 {info['match_score']:.0%}")

    # ===== 第二步: 模糊搜索 =====
    if not info:
        print(f"  [Step 2] Semantic Scholar 模糊搜索...")
        info = step2_fuzzy_search(title)
        if info:
            print(f"    -> 命中! 匹配度 {info['match_score']:.0%}")

    # ===== 兜底: arXiv =====
    if not info:
        print(f"  [Step 2b] arXiv 兜底搜索...")
        info = step2b_arxiv_search(title)
        if info:
            print(f"    -> 命中! 匹配度 {info['match_score']:.0%}")

    if not info:
        result["reason"] = "所有搜索源均未找到"
        print(f"  ❌ {result['reason']}")
        return result

    # 打印元数据
    print(f"  论文: {info['title'][:55]}...")
    print(f"  来源: {info['source']}")
    if info.get("venue"):
        print(f"  会议: {info['venue']} {info.get('year', '')}")
    if info.get("arxiv_id"):
        print(f"  arXiv: {info['arxiv_id']}")
    if info.get("authors"):
        print(f"  作者: {', '.join(info['authors'][:3])}")

    # ===== 第三步: 级联下载 =====
    print(f"  [Step 3] 级联下载...")
    temp_path = str(OUTPUT_DIR / "temp.pdf")
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not step3_cascade_download(info, title, temp_path):
        result["reason"] = "所有下载源均失败"
        print(f"  ❌ {result['reason']}")
        return result

    # ===== 内容校验 =====
    print(f"  [校验] pypdf 首页验证...")
    if not step3_validate(temp_path, title):
        result["reason"] = "首页校验失败（下载到错误论文）"
        print(f"  ❌ {result['reason']}")
        os.remove(temp_path)
        return result

    # ===== 第四步: 重命名 =====
    filename = step4_rename(info)
    final_path = OUTPUT_DIR / filename
    counter = 1
    while final_path.exists():
        filename = step4_rename(info).replace(".pdf", f" ({counter}).pdf")
        final_path = OUTPUT_DIR / filename
        counter += 1

    os.rename(temp_path, final_path)
    result["status"] = "success"
    result["filename"] = filename
    print(f"  ✅ {filename}")
    return result


def main():
    parser = argparse.ArgumentParser(description="论文下载器 v4")
    parser.add_argument("titles", nargs="*", help="论文标题")
    parser.add_argument("--file", "-f", type=str, help="论文标题文件（每行一个）")
    parser.add_argument("--output", "-o", type=str, default="./downloaded_papers", help="输出目录")
    args = parser.parse_args()

    titles = []
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        titles.append(line)
        except FileNotFoundError:
            print(f"错误: 文件不存在 {args.file}")
            sys.exit(1)
    titles.extend(args.titles)
    if not titles:
        parser.print_help()
        sys.exit(1)

    global OUTPUT_DIR
    OUTPUT_DIR = Path(args.output)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"{'='*60}")
    print(f"  论文下载器 v4 - Academic Paper Downloader")
    print(f"{'='*60}")
    print(f"  搜索: Semantic Scholar (精准+模糊) -> arXiv")
    print(f"  下载: OpenAccessPdf -> OpenReview -> PMLR -> arXiv")
    print(f"  校验: pypdf 首页关键词验证")
    print(f"  输出: {OUTPUT_DIR.absolute()}")
    print(f"  数量: {len(titles)}")
    print(f"{'='*60}")

    results = []
    for i, title in enumerate(titles, 1):
        r = process_paper(title, i, len(titles))
        results.append(r)

    # ===== 报告 =====
    ok = [r for r in results if r["status"] == "success"]
    fail = [r for r in results if r["status"] == "failed"]

    print(f"\n{'='*60}")
    print(f"  下载报告")
    print(f"{'='*60}")
    print(f"  成功: {len(ok)}/{len(titles)}")
    print(f"  失败: {len(fail)}/{len(titles)}")
    if ok:
        print(f"\n  ✅ 成功:")
        for r in ok:
            print(f"     {r['filename']}")
    if fail:
        print(f"\n  ❌ 失败:")
        for r in fail:
            print(f"     {r['title'][:50]}... -> {r['reason']}")
    print(f"\n  输出: {OUTPUT_DIR.absolute()}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
