import feedparser
import requests
import git
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time

USERNAME = "mi_nini"

repo_path = '.'
BASE_DIR = "velog-posts"
posts_dir = os.path.join(repo_path, BASE_DIR)
os.makedirs(posts_dir, exist_ok=True)

repo = git.Repo(repo_path)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


# ---------------------------
# 1. Velog 프로필 페이지에서 전체 글 목록 스크래핑
# ---------------------------
def get_all_posts():
    all_posts = []
    page = 1

    while True:
        url = f"https://velog.io/@{USERNAME}?page={page}"
        print(f"Fetching post list page {page}...")

        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            res.raise_for_status()
        except Exception as e:
            print(f"Failed: {e}")
            break

        soup = BeautifulSoup(res.text, "html.parser")

        # 글 카드 셀렉터
        cards = soup.select("div.FlatPostCard_block__a1YEv") or \
                soup.select("div[class*='FlatPostCard']") or \
                soup.select("div[class*='PostCard']")

        if not cards:
            print(f"No cards found at page {page}. Done.")
            break

        for card in cards:
            a_tag = card.select_one("a")
            title_tag = card.select_one("h2") or card.select_one("h4")
            date_tag = card.select_one("span.date") or card.select_one("span[class*='date']")

            if not a_tag:
                continue

            link = "https://velog.io" + a_tag["href"] if a_tag["href"].startswith("/") else a_tag["href"]
            title = title_tag.get_text(strip=True) if title_tag else link.split("/")[-1]
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            all_posts.append({
                "title": title,
                "link": link,
                "date_str": date_str,
            })

        print(f"Loaded {len(all_posts)} posts so far...")
        page += 1
        time.sleep(0.5)

    return all_posts


# ---------------------------
# 2. 글 본문 스크래핑
# ---------------------------
def get_post_body(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        res.raise_for_status()
    except Exception as e:
        print(f"Fetch failed: {e}")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    body = soup.select_one("div.sc-dAlyuH") or \
           soup.select_one("div[class*='MarkdownRender']") or \
           soup.select_one("div[class*='atom-one']") or \
           soup.select_one("article")

    return body.get_text(separator="\n").strip() if body else None


# ---------------------------
# 3. 날짜 파싱
# ---------------------------
def parse_date(date_str):
    for fmt in ["%Y-%m-%d", "%B %d, %Y", "%Y년 %m월 %d일"]:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            pass
    return datetime.now()


# ---------------------------
# 4. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 5. 메인 로직
# ---------------------------
def main():
    # RSS에서 최근 20개 먼저 가져오기 (날짜 정보 정확)
    rss_entries = {}
    feed = feedparser.parse(f'https://api.velog.io/rss/@{USERNAME}')
    for entry in feed.entries:
        rss_entries[entry.link] = entry
    print(f"RSS entries loaded: {len(rss_entries)}")

    # 전체 글 목록 스크래핑
    posts = get_all_posts()
    print(f"\nTotal posts found: {len(posts)}")

    if not posts:
        print("No posts fetched. Exiting.")
        return

    changed = False

    for post in posts:
        title = post["title"]
        link = post["link"]

        # RSS에 있으면 RSS 날짜 사용, 없으면 스크래핑 날짜 사용
        if link in rss_entries:
            entry = rss_entries[link]
            date = datetime(*entry.published_parsed[:6])
        else:
            date = parse_date(post["date_str"])

        year = str(date.year)
        month = str(date.month).zfill(2)

        post_dir = os.path.join(posts_dir, year, month)
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

        repo.git.add(file_path)
        repo.git.commit('-m', f'Add/Update post: {title}')
        changed = True

        time.sleep(1)  # 스크래핑 간격

    if changed:
        repo.git.push()
        print("Pushed to GitHub.")
    else:
        print("No changes to push.")


if __name__ == "__main__":
    main()
