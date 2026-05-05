import feedparser
import requests
import git
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time

USERNAME = "mi_nini"
GRAPHQL_URL = "https://v2.velog.io/graphql"

repo_path = '.'
BASE_DIR = "velog-posts"
posts_dir = os.path.join(repo_path, BASE_DIR)
os.makedirs(posts_dir, exist_ok=True)

repo = git.Repo(repo_path)


# ---------------------------
# 1. GraphQL로 전체 글 목록 가져오기
# ---------------------------
def get_all_posts():
    all_posts = []
    cursor = None

    while True:
        # cursor 없을 때와 있을 때 쿼리 분리
        if cursor:
            query = """
            query {
              posts(username: "%s", cursor: "%s") {
                id
                title
                released_at
                url_slug
                is_private
              }
            }
            """ % (USERNAME, cursor)
        else:
            query = """
            query {
              posts(username: "%s") {
                id
                title
                released_at
                url_slug
                is_private
              }
            }
            """ % USERNAME

        try:
            res = requests.post(
                GRAPHQL_URL,
                json={"query": query},
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            print(f"GraphQL status: {res.status_code}")
            json_res = res.json()
        except Exception as e:
            print(f"Request failed: {e}")
            break

        if "errors" in json_res:
            print(f"GraphQL errors: {json_res['errors']}")
            break

        if "data" not in json_res or not json_res["data"]:
            print(f"Unexpected response: {json_res}")
            break

        posts = json_res["data"].get("posts", [])
        if not posts:
            break

        # 공개 글만 필터
        public_posts = [p for p in posts if not p.get("is_private", False)]
        all_posts.extend(public_posts)
        cursor = posts[-1]["id"]

        print(f"Loaded {len(all_posts)} posts (cursor: {cursor[:8]}...)")
        time.sleep(0.5)

    return all_posts


# ---------------------------
# 2. RSS에서 최근 20개 본문 가져오기 (빠름)
# ---------------------------
def get_rss_bodies():
    feed = feedparser.parse(f'https://api.velog.io/rss/@{USERNAME}')
    bodies = {}
    for entry in feed.entries:
        soup = BeautifulSoup(entry.description, "html.parser")
        bodies[entry.link] = soup.get_text(separator="\n").strip()
    print(f"RSS bodies loaded: {len(bodies)}")
    return bodies


# ---------------------------
# 3. 글 본문 직접 스크래핑 (RSS에 없는 오래된 글)
# ---------------------------
def scrape_body(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Velog 본문 셀렉터 여러 개 시도
        body = (
            soup.select_one("div.sc-dAlyuH") or
            soup.select_one("div[class*='MarkdownRender']") or
            soup.select_one("div[class*='atom-one']") or
            soup.select_one("article")
        )
        return body.get_text(separator="\n").strip() if body else None
    except Exception as e:
        print(f"Scrape failed ({url}): {e}")
        return None


# ---------------------------
# 4. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 5. 메인 로직
# ---------------------------
def main():
    # GraphQL로 전체 글 목록 시도
    posts = get_all_posts()

    # GraphQL 실패 시 RSS fallback
    if not posts:
        print("GraphQL failed. Falling back to RSS only (20 posts)...")
        feed = feedparser.parse(f'https://api.velog.io/rss/@{USERNAME}')
        for entry in feed.entries:
            try:
                date = datetime(*entry.published_parsed[:6])
            except:
                date = datetime.now()
            posts.append({
                "title": entry.title,
                "url_slug": entry.link.split("/")[-1],
                "released_at": date.isoformat() + "Z",
                "is_private": False,
                "_link": entry.link,
                "_body": BeautifulSoup(entry.description, "html.parser").get_text(separator="\n").strip()
            })

    print(f"\nTotal posts: {len(posts)}")

    if not posts:
        print("No posts fetched. Exiting.")
        return

    # RSS 본문 미리 로드 (속도 최적화)
    rss_bodies = get_rss_bodies()

    changed = False

    for post in posts:
        title = post["title"]
        slug = post.get("url_slug", "")
        link = post.get("_link") or f"https://velog.io/@{USERNAME}/{slug}"

        try:
            date = datetime.fromisoformat(
                post["released_at"].replace("Z", "+00:00")
            )
        except:
            date = datetime.now()

        year = str(date.year)
        month = str(date.month).zfill(2)

        post_dir = os.path.join(posts_dir, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date.strftime('%Y-%m-%d')}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # 본문: RSS → 스크래핑 순으로 시도
        body = post.get("_body") or rss_bodies.get(link) or scrape_body(link)

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

        time.sleep(0.5)

    if changed:
        repo.git.push()
        print("Pushed to GitHub.")
    else:
        print("No changes to push.")


if __name__ == "__main__":
    main()
