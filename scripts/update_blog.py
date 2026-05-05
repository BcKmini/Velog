import requests
import os
import re
from datetime import datetime
import time

USERNAME = "mi_nini"
BASE_DIR = "velog-posts"

os.makedirs(BASE_DIR, exist_ok=True)

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
        cursor = posts[-1]["id"]

        print(f"Loaded {len(all_posts)} posts...")
        time.sleep(0.3)

    return all_posts


def get_post_detail(slug):
    url = "https://v2.velog.io/graphql"

    query = """
    query Post($username: String!, $url_slug: String!) {
      post(username: $username, url_slug: $url_slug) {
        title
        released_at
        updated_at
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


def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


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
        updated_at = detail.get("updated_at")
        if updated_at:
            updated_date = datetime.fromisoformat(
                updated_at.replace("Z", "+00:00")
            )
        else:
            updated_date = date

        year = str(date.year)
        month = str(date.month).zfill(2)

        post_dir = os.path.join(BASE_DIR, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date.strftime('%Y-%m-%d')}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        new_content = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')}
updated: {updated_date.strftime('%Y-%m-%d %H:%M:%S')}
---

{body}
"""

        # 파일이 없거나 내용이 다르면 저장 (수정된 글도 반영)
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

        time.sleep(0.2)


if __name__ == "__main__":
    main()
