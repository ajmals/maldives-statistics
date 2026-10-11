"""
scripts/download_yearbooks.py

Downloads Statistical Yearbook data (PDFs, Excel spreadsheets, and table files)
from https://statisticsmaldives.gov.mv/yearbook/ into organized directories
under data/raw/<year>/<chapter>/.

Features:
- Discovers and parses all available yearbooks (2008-2026)
- Automatically categorizes files into clean chapter folders (e.g., '1.0 Geography', '10.0 Tourism')
- Unescapes HTML entities and safely encodes URI components
- Automatic extension fallback (.xlsx <-> .xls) for broken ministry links
- Fast multi-threaded concurrent downloading with retry logic
- Resumable: skips already downloaded files
- Generates manifest.json per year and a consolidated data/raw/manifest.json
"""

import os
import sys
import re
import ssl
import json
import html
import time
import argparse
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Canonical chapter mapping by chapter number prefix
CHAPTER_MAP = {
    "1": "1.0 Geography",
    "2": "2.0 Environment",
    "3": "3.0 Population",
    "4": "4.0 Housing and public infrastructure",
    "5": "5.0 Employment",
    "6": "6.0 Health",
    "7": "7.0 Education",
    "8": "8.0 Law & Order",
    "9": "9.0 Fisheries & Agriculture",
    "10": "10.0 Tourism",
    "11": "11.0 Transport and Communication",
    "12": "12.0 Electricity and water",
    "13": "13.0 Public Finance",
    "14": "14.0 Money and banking",
    "15": "15.0 Foreign trade & Balance of payments",
    "16": "16.0 National Accounts",
    "17": "17.0 Prices",
    "18": "18.0 Pension & social protection",
    "19": "19.0 Human rights",
    "20": "20.0 Political parties & Election",
}

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

SSL_CTX = create_ssl_context()

def fetch_url_text(url, timeout=15, retries=3):
    url = clean_and_encode_url(url)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as response:
                return response.read().decode("utf-8", errors="ignore")
        except Exception:
            if attempt == retries - 1:
                return ""
            time.sleep(1.0)
    return ""

def clean_and_encode_url(raw_url):
    raw_url = html.unescape(raw_url).strip()
    parts = urllib.parse.urlsplit(raw_url)
    escaped_path = urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/:@!$&'()*+,;=")
    escaped_query = urllib.parse.quote(urllib.parse.unquote(parts.query), safe="/:@!$&'()*+,;=?")
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, escaped_path, escaped_query, parts.fragment))

def clean_name(name):
    name = re.sub(r"<[^>]+>", "", name)
    name = re.sub(r"&[a-zA-Z0-9#]+;", " ", name)
    name = re.sub(r"[\r\n\t]+", " ", name)
    name = name.strip()
    return name

def infer_chapter_folder(filename, sector_hint=""):
    """Determines the appropriate folder name for a given file."""
    clean_hint = clean_name(sector_hint).lower()
    
    if "indicator" in filename.lower() or "indicator" in clean_hint:
        return "indicators"
    if "pocketbook" in filename.lower() or "pocketbook" in clean_hint or "spom" in filename.lower():
        return "indicators"
        
    m = re.match(r"^(\d{1,2})\.", filename)
    if m:
        ch_num = m.group(1)
        if ch_num in CHAPTER_MAP:
            return CHAPTER_MAP[ch_num]
            
    hint_keywords = {
        "geography": "1.0 Geography",
        "environment": "2.0 Environment",
        "population": "3.0 Population",
        "housing": "4.0 Housing and public infrastructure",
        "employment": "5.0 Employment",
        "health": "6.0 Health",
        "education": "7.0 Education",
        "law": "8.0 Law & Order",
        "order": "8.0 Law & Order",
        "fisheries": "9.0 Fisheries & Agriculture",
        "agriculture": "9.0 Fisheries & Agriculture",
        "tourism": "10.0 Tourism",
        "transport": "11.0 Transport and Communication",
        "communication": "11.0 Transport and Communication",
        "electricity": "12.0 Electricity and water",
        "water": "12.0 Electricity and water",
        "public finance": "13.0 Public Finance",
        "finance": "13.0 Public Finance",
        "money": "14.0 Money and banking",
        "banking": "14.0 Money and banking",
        "foreign trade": "15.0 Foreign trade & Balance of payments",
        "trade": "15.0 Foreign trade & Balance of payments",
        "national accounts": "16.0 National Accounts",
        "accounts": "16.0 National Accounts",
        "prices": "17.0 Prices",
        "pension": "18.0 Pension & social protection",
        "human rights": "19.0 Human rights",
        "political": "20.0 Political parties & Election",
        "election": "20.0 Political parties & Election",
    }
    for kw, ch_name in hint_keywords.items():
        if kw in clean_hint:
            return ch_name
            
    if clean_hint:
        return clean_name(sector_hint)
    return "general"

def extract_links_modern_wp(year, base_url, html_text):
    items = []
    panel_pattern = re.compile(r'<div class="sector-panel[^"]*"[^>]*>(.*?)</div>\s*(?=<div class="sector-panel|$)', re.DOTALL)
    panels = panel_pattern.findall(html_text)
    
    if panels:
        for panel in panels:
            title_m = re.search(r'<div class="sector-panel-title"[^>]*>(.*?)</div>', panel, re.DOTALL)
            sector_title = title_m.group(1).strip() if title_m else ""
            
            for link_m in re.finditer(r'href=[\"\']([^\"\'#\s]+)[\"\']', panel):
                href = html.unescape(link_m.group(1))
                abs_url = urllib.parse.urljoin(base_url, href)
                if any(abs_url.lower().endswith(ext) for ext in [".pdf", ".xls", ".xlsx"]):
                    fname = os.path.basename(urllib.parse.urlparse(abs_url).path)
                    folder = infer_chapter_folder(fname, sector_title)
                    items.append({
                        "year": year,
                        "url": abs_url,
                        "filename": fname,
                        "folder": folder,
                        "sector": clean_name(sector_title)
                    })
    else:
        for link_m in re.finditer(r'href=[\"\']([^\"\'#\s]+)[\"\']', html_text):
            href = html.unescape(link_m.group(1))
            abs_url = urllib.parse.urljoin(base_url, href)
            if any(abs_url.lower().endswith(ext) for ext in [".pdf", ".xls", ".xlsx"]):
                fname = os.path.basename(urllib.parse.urlparse(abs_url).path)
                folder = infer_chapter_folder(fname, "")
                items.append({
                    "year": year,
                    "url": abs_url,
                    "filename": fname,
                    "folder": folder,
                    "sector": folder
                })
                
    return items

def extract_links_multipage_wp(year, base_url, html_text):
    items = []
    hrefs = [html.unescape(h) for h in re.findall(r'href=[\"\']([^\"\'#\s]+)[\"\']', html_text)]
    
    for h in hrefs:
        abs_url = urllib.parse.urljoin(base_url, h)
        if any(abs_url.lower().endswith(ext) for ext in [".pdf", ".xls", ".xlsx"]):
            fname = os.path.basename(urllib.parse.urlparse(abs_url).path)
            folder = infer_chapter_folder(fname, "general")
            items.append({
                "year": year,
                "url": abs_url,
                "filename": fname,
                "folder": folder,
                "sector": "general"
            })
            
    subpages = set()
    for h in hrefs:
        abs_url = urllib.parse.urljoin(base_url, h)
        if f"yearbook/{year}/" in abs_url and not any(x in abs_url for x in ["wp-", "xmlrpc", "feed", "themes", "css", "js"]):
            subpages.add(abs_url)
            
    for sp in sorted(subpages):
        sp_html = fetch_url_text(sp)
        if not sp_html:
            continue
        sp_path = urllib.parse.urlparse(sp).path.strip("/").split("/")[-1]
        sp_hrefs = [html.unescape(h) for h in re.findall(r'href=[\"\']([^\"\'#\s]+)[\"\']', sp_html)]
        for h in sp_hrefs:
            abs_url = urllib.parse.urljoin(sp, h)
            if any(abs_url.lower().endswith(ext) for ext in [".pdf", ".xls", ".xlsx"]):
                fname = os.path.basename(urllib.parse.urlparse(abs_url).path)
                folder = infer_chapter_folder(fname, sp_path)
                items.append({
                    "year": year,
                    "url": abs_url,
                    "filename": fname,
                    "folder": folder,
                    "sector": sp_path
                })
                
    return items

def extract_links_static_html(year, base_url, html_text):
    items = []
    
    hrefs = [html.unescape(h) for h in re.findall(r'href=[\"\']([^\"\'#\s]+)[\"\']', html_text)]
    for h in hrefs:
        abs_url = urllib.parse.urljoin(base_url, h)
        if any(abs_url.lower().endswith(ext) for ext in [".pdf", ".xls", ".xlsx", ".zip", ".htm", ".html"]):
            fname = os.path.basename(urllib.parse.urlparse(abs_url).path)
            if fname.lower() in ["yearbook.html", "index.html", "foreword.html", "introduction.html", "feedback.html", "credits.html", "acknowledgement.html", "explanatory.html", "others.html"]:
                continue
            path_parts = urllib.parse.urlparse(abs_url).path.strip("/").split("/")
            hint = path_parts[-2] if len(path_parts) > 1 else ""
            folder = infer_chapter_folder(fname, hint)
            items.append({
                "year": year,
                "url": abs_url,
                "filename": fname,
                "folder": folder,
                "sector": hint or folder
            })
            
    # Robust dTree parser for 2010 and 2011
    dtree_links = re.findall(r"d\.add\(\s*\d+\s*,\s*-?\d+\s*,\s*'(?:[^'\\]|\\.)*'\s*,\s*'([^']+)'", html_text)
    for d in dtree_links:
        d = html.unescape(d).strip()
        if not d:
            continue
        abs_url = urllib.parse.urljoin(base_url, d)
        if any(abs_url.lower().endswith(ext) for ext in [".pdf", ".xls", ".xlsx", ".htm", ".html"]):
            fname = os.path.basename(urllib.parse.urlparse(abs_url).path)
            path_parts = urllib.parse.urlparse(abs_url).path.strip("/").split("/")
            hint = path_parts[-2] if len(path_parts) > 1 else ""
            folder = infer_chapter_folder(fname, hint)
            items.append({
                "year": year,
                "url": abs_url,
                "filename": fname,
                "folder": folder,
                "sector": hint or folder
            })
            
    return items

def discover_yearbook_files(year):
    y_int = int(year)
    if y_int >= 2019:
        base_url = f"https://statisticsmaldives.gov.mv/yearbook/{year}/"
        html_text = fetch_url_text(base_url)
        raw_items = extract_links_modern_wp(year, base_url, html_text)
    elif 2016 <= y_int <= 2018:
        base_url = f"https://statisticsmaldives.gov.mv/yearbook/{year}/"
        html_text = fetch_url_text(base_url)
        raw_items = extract_links_multipage_wp(year, base_url, html_text)
    elif y_int == 2015:
        base_url = "https://statisticsmaldives.gov.mv/yearbook2015/index.html"
        html_text = fetch_url_text(base_url)
        raw_items = extract_links_static_html(year, base_url, html_text)
    elif y_int in [2014, 2013, 2012, 2010]:
        base_url = f"https://statisticsmaldives.gov.mv/yearbook{year}/yearbook.html"
        html_text = fetch_url_text(base_url)
        raw_items = extract_links_static_html(year, base_url, html_text)
    elif y_int == 2011:
        base_url = "https://statisticsmaldives.gov.mv/YearBook2011/yearbook.html"
        html_text = fetch_url_text(base_url)
        raw_items = extract_links_static_html(year, base_url, html_text)
    elif y_int in [2009, 2008]:
        base_url = f"https://statisticsmaldives.gov.mv/yearbook{year}/index.html"
        html_text = fetch_url_text(base_url)
        raw_items = extract_links_static_html(year, base_url, html_text)
    else:
        return []

    seen_urls = set()
    deduped = []
    for it in raw_items:
        u = it["url"]
        if u not in seen_urls:
            seen_urls.add(u)
            deduped.append(it)
    return deduped

def download_file(item, output_root, skip_existing=True):
    year = item["year"]
    folder = item["folder"]
    filename = urllib.parse.unquote(item["filename"])
    target_dir = os.path.join(output_root, year, folder)
    target_path = os.path.join(target_dir, filename)
    url = clean_and_encode_url(item["url"])
    
    os.makedirs(target_dir, exist_ok=True)
    
    if skip_existing and os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return {
            "status": "skipped",
            "url": url,
            "path": target_path,
            "size": os.path.getsize(target_path),
            "year": year,
            "folder": folder,
            "filename": filename
        }
        
    retries = 3
    candidate_urls = [url]
    # Fallback between .xlsx and .xls if one fails
    if url.lower().endswith(".xlsx"):
        candidate_urls.append(url[:-1]) # .xls
    elif url.lower().endswith(".xls"):
        candidate_urls.append(url + "x") # .xlsx

    last_error = ""
    for cur_url in candidate_urls:
        for attempt in range(retries):
            try:
                req = urllib.request.Request(cur_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, context=SSL_CTX, timeout=25) as resp:
                    data = resp.read()
                    with open(target_path, "wb") as f:
                        f.write(data)
                return {
                    "status": "downloaded",
                    "url": cur_url,
                    "path": target_path,
                    "size": len(data),
                    "year": year,
                    "folder": folder,
                    "filename": filename
                }
            except Exception as e:
                last_error = str(e)
                time.sleep(0.5 + attempt * 0.5)

    return {
        "status": "failed",
        "error": last_error,
        "url": url,
        "path": target_path,
        "year": year,
        "folder": folder,
        "filename": filename
    }

def process_year(year, output_root, concurrency=8, skip_existing=True):
    print(f"\n=======================================================")
    print(f"  Processing Yearbook {year} ...")
    print(f"=======================================================")
    
    items = discover_yearbook_files(year)
    print(f"Found {len(items)} downloadable items for {year}.")
    if not items:
        return []

    results = []
    downloaded_cnt = 0
    skipped_cnt = 0
    failed_cnt = 0
    total_bytes = 0

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_map = {executor.submit(download_file, it, output_root, skip_existing): it for it in items}
        for future in as_completed(future_map):
            res = future.result()
            results.append(res)
            st = res.get("status")
            if st == "downloaded":
                downloaded_cnt += 1
                total_bytes += res.get("size", 0)
                sys.stdout.write(f"\r[{year}] Progress: {downloaded_cnt + skipped_cnt + failed_cnt}/{len(items)} | New: {downloaded_cnt} | Skipped: {skipped_cnt} | Failed: {failed_cnt}")
                sys.stdout.flush()
            elif st == "skipped":
                skipped_cnt += 1
                total_bytes += res.get("size", 0)
                sys.stdout.write(f"\r[{year}] Progress: {downloaded_cnt + skipped_cnt + failed_cnt}/{len(items)} | New: {downloaded_cnt} | Skipped: {skipped_cnt} | Failed: {failed_cnt}")
                sys.stdout.flush()
            else:
                failed_cnt += 1

    print(f"\nCompleted {year}: {downloaded_cnt} downloaded, {skipped_cnt} cached/skipped, {failed_cnt} failed ({total_bytes / (1024*1024):.2f} MB)")
    
    manifest_path = os.path.join(output_root, year, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "year": year,
            "total_items": len(items),
            "downloaded": downloaded_cnt,
            "skipped": skipped_cnt,
            "failed": failed_cnt,
            "total_size_bytes": total_bytes,
            "items": results
        }, f, indent=2)
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Download Statistical Yearbook archives")
    parser.add_argument("--years", type=str, default="all", help="Comma-separated years e.g. '2026,2025' or 'all'")
    parser.add_argument("--output", type=str, default="data/raw", help="Base output directory")
    parser.add_argument("--concurrency", type=int, default=8, help="Number of download threads")
    parser.add_argument("--force", action="store_true", help="Force re-download existing files")
    args = parser.parse_args()

    if args.years == "all":
        years = [str(y) for y in range(2008, 2027)]
    else:
        years = [y.strip() for y in args.years.split(",") if y.strip()]

    print(f"Target years: {years}")
    print(f"Output directory: {args.output}")
    print(f"Concurrency: {args.concurrency}")
    
    os.makedirs(args.output, exist_ok=True)
    all_year_summaries = {}
    
    for y in sorted(years, reverse=True):
        y_results = process_year(y, args.output, concurrency=args.concurrency, skip_existing=not args.force)
        all_year_summaries[y] = {
            "total": len(y_results),
            "downloaded": sum(1 for r in y_results if r.get("status") == "downloaded"),
            "skipped": sum(1 for r in y_results if r.get("status") == "skipped"),
            "failed": sum(1 for r in y_results if r.get("status") == "failed"),
            "size_mb": sum(r.get("size", 0) for r in y_results) / (1024 * 1024)
        }

    summary_path = os.path.join(args.output, "manifest.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_year_summaries, f, indent=2)
        
    print("\n=======================================================")
    print("  ALL DOWNLOADS COMPLETED!")
    print("=======================================================")
    for y, s in all_year_summaries.items():
        print(f"Year {y}: {s['total']} files | {s['size_mb']:.2f} MB (downloaded: {s['downloaded']}, cached: {s['skipped']}, failed: {s['failed']})")

if __name__ == "__main__":
    main()
