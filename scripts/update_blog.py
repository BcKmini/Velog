import requests
import os
import re
from datetime import datetime
import time

USERNAME = "mi_nini"
BASE_DIR = "velog-posts"

os.makedirs(BASE_DIR, exist_ok=True)

# ---------------------------
# 1. 전체 글 가져오기 (cursor 방식으로 변경)
# ---------------------------
def get_all_posts():
    url = "https://v2.velog.io/graphql"
    all_posts = []
    cursor = None
    LIMIT = 20

    while True:
        query = """
        query Posts($username: String!, $limit: Int!, $cursor: String) {
          posts(username: $username, limit: $limit, cursor: $cursor) {
            id
            title
            released_at
            url_slug
          }
        }
        """

        variables = {
            "username": USERNAME,
            "limit": LIMIT,
        }
        if cursor:
            variables["cursor"] = cursor

        try:
            res = requests.post(
                url,
                json={"query": query, "variables": variables},
                timeout=15
            )
            res.raise_for_status()
            json_res = res.json()
        except Exception as e:
            print(f"Request failed: {e}")
            break

        # 응답 구조 확인용 디버깅
        if "errors" in json_res:
            print(f"GraphQL errors: {json_res['errors']}")
            break

        if "data" not in json_res or json_res["data"] is None:
            print(f"Unexpected response: {json_res}")
            break

        posts = json_res["data"].get("posts", [])

        if not posts:
            break

        all_posts.extend(posts)

        # 다음 페이지 cursor = 마지막 글의 id
        cursor = posts[-1]["id"]

        print(f"Loaded {len(all_posts)} posts...")
        time.sleep(0.3)

    return all_posts


# ---------------------------
# 2. 글 상세 가져오기
# ---------------------------
def get_post_detail(slug):
    url = "https://v2.velog.io/graphql"

    query = """
    query Post($username: String!, $url_slug: String!) {
      post(username: $username, url_slug: $url_slug) {
        title
        released_at
        body
      }
    }
    """

    try:
        res = requests.post(
            url,
            json={
                "query": query,
                "variables": {
                    "username": USERNAME,
                    "url_slug": slug
                }
            },
            timeout=15
        )
        res.raise_for_status()
        json_res = res.json()
    except Exception as e:
        print(f"Request failed for {slug}: {e}")
        return None

    if "errors" in json_res:
        print(f"GraphQL errors for {slug}: {json_res['errors']}")
        return None

    if "data" not in json_res or json_res["data"] is None:
        print(f"Unexpected response for {slug}: {json_res}")
        return None

    return json_res["data"].get("post")


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

    if not posts:
        print("No posts fetched. Exiting.")
        return

    print(f"Total posts: {len(posts)}")

    for post in posts:
        slug = post["url_slug"]

        detail = get_post_detail(slug)

        if not detail or not detail.get("body"):
            print(f"Skip (no detail): {slug}")
            continue

        title = detail["title"]
        body = detail["body"]

        date = datetime.fromisoformat(
            detail["released_at"].replace("Z", "+00:00")
        )

        year = str(date.year)
        month = str(date.month).zfill(2)

        # 폴더 생성
        post_dir = os.path.join(BASE_DIR, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date.strftime('%Y-%m-%d')}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # 이미 있으면 skip
        if os.path.exists(file_path):
            print(f"Already exists, skip: {file_name}")
            continue

        markdown = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')}
---

{body}
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved: {file_name}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
