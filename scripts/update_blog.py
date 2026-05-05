import feedparser
import requests
import git
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time

USERNAME = "mi_nini"
rss_url = f'https://api.velog.io/rss/@{USERNAME}'
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
        query = """
        query Posts($username: String!, $cursor: String) {
          posts(username: $username, cursor: $cursor) {
            id
            title
            released_at
            url_slug
            is_private
          }
        }
        """
        variables = {"username": USERNAME}
        if cursor:
            variables["cursor"] = cursor

        try:
            res = requests.post(
                GRAPHQL_URL,
                json={"query": query, "variables": variables},
                timeout=15
            )
            res.raise_for_status()
            json_res = res.json()
        except Exception as e:
            print(f"Request failed: {e}")
            break

        if "errors" in json_res:
            print(f"GraphQL errors: {json_res['errors']}")
            break

        if "data" not in json_res or json_res["data"] is None:
            print(f"Unexpected response: {json_res}")
            break

        posts = json_res["data"].get("posts", [])
        if not posts:
            break

        # 임시저장(비공개) 글 제외
        public_posts = [p for p in posts if not p.get("is_private", False)]
        all_posts.extend(public_posts)
        cursor = posts[-1]["id"]

        print(f"Loaded {len(all_posts)} posts...")
        time.sleep(0.3)

    return all_posts


# ---------------------------
# 2. 글 본문 가져오기 (GraphQL)
# ---------------------------
def get_post_body(slug):
    query = """
    query Post($username: String!, $url_slug: String!) {
      post(username: $username, url_slug: $url_slug) {
        body
      }
    }
    """
    try:
        res = requests.post(
            GRAPHQL_URL,
            json={
                "query": query,
                "variables": {"username": USERNAME, "url_slug": slug}
            },
            timeout=15
        )
        res.raise_for_status()
        json_res = res.json()
        return json_res["data"]["post"]["body"]
    except Exception as e:
        print(f"Body fetch failed for {slug}: {e}")
        return None


# ---------------------------
# 3. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 4. 메인 로직
# ---------------------------
def main():
    posts = get_all_posts()
    print(f"\nTotal public posts: {len(posts)}")

    if not posts:
        print("No posts fetched. Exiting.")
        return

    changed = False

    for post in posts:
        title = post["title"]
        slug = post["url_slug"]

        date = datetime.fromisoformat(
            post["released_at"].replace("Z", "+00:00")
        )

        year = str(date.year)
        month = str(date.month).zfill(2)

        post_dir = os.path.join(posts_dir, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date.strftime('%Y-%m-%d')}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # 본문 가져오기
        body = get_post_body(slug)
        if not body:
            print(f"Skip (no body): {title}")
            continue

        link = f"https://velog.io/@{USERNAME}/{slug}"

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

        time.sleep(0.3)

    if changed:
        repo.git.push()
        print("Pushed to GitHub.")
    else:
        print("No changes to push.")


if __name__ == "__main__":
    main()
