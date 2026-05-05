import requests
import os
import re
from datetime import datetime
import time
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

USERNAME = "mi_nini"
BASE_DIR = "velog-posts"
RSS_URL = f"https://v2.velog.io/rss/{USERNAME}"

os.makedirs(BASE_DIR, exist_ok=True)


# ---------------------------
# 1. RSS로 전체 글 목록 가져오기
# ---------------------------
def get_all_posts():
    try:
        res = requests.get(RSS_URL, timeout=15)
        res.raise_for_status()
        print(f"RSS status: {res.status_code}")
        print(f"RSS content preview: {res.text[:500]}")
    except Exception as e:
        print(f"RSS fetch failed: {e}")
        return []

    try:
        root = ET.fromstring(res.content)
    except Exception as e:
        print(f"XML parse failed: {e}")
        return []

    channel = root.find("channel")
    if channel is None:
        print("No channel found in RSS")
        return []

    posts = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()

        if not link:
            continue

        posts.append({
            "title": title,
            "link": link,
            "pub_date": pub_date,
        })

    print(f"Total posts from RSS: {len(posts)}")
    return posts


# ---------------------------
# 2. 글 상세 내용 스크래핑
# ---------------------------
def get_post_body(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
    except Exception as e:
        print(f"Fetch failed for {url}: {e}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    # Velog 본문 셀렉터
    body = soup.select_one("div.sc-dAlyuH") or \
           soup.select_one("div[class*='atom-one']") or \
           soup.select_one("div.velog-markdown-body") or \
           soup.select_one("div[class*='MarkdownRender']") or \
           soup.select_one("article")

    if body:
        return body.get_text(separator="\n").strip()

    print(f"Body not found for {url}")
    return None


# ---------------------------
# 3. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 4. 날짜 파싱
# ---------------------------
def parse_date(pub_date_str):
    # RSS pubDate 형식: "Mon, 01 Jan 2024 00:00:00 GMT"
    try:
        return datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
    except:
        pass
    try:
        return datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S +0000")
    except:
        pass
    return datetime.now()


# ---------------------------
# 5. 메인 로직
# ---------------------------
def main():
    posts = get_all_posts()

    if not posts:
        print("No posts fetched. Exiting.")
        return

    for post in posts:
        title = post["title"]
        link = post["link"]
        pub_date = post["pub_date"]

        date = parse_date(pub_date)

        year = str(date.year)
        month = str(date.month).zfill(2)

        post_dir = os.path.join(BASE_DIR, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date.strftime('%Y-%m-%d')}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # 본문 가져오기
        body = get_post_body(link)
        if not body:
            print(f"Skip (no body): {title}")
            continue

        new_content = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')}
source: "{link}"
---

{body}
"""

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing = f.read()
            if existing == new_content:
                print(f"No change, skip: {file_name}")
                continue
            else:
                print(f"Updated: {file_name}")
        else:
            print(f"New post: {file_name}")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        time.sleep(1)  # 스크래핑 간격


if __name__ == "__main__":
    main()
