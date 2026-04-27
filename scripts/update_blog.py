import requests
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import time

USERNAME = "mi_nini"
BASE_DIR = "velog-posts"

os.makedirs(BASE_DIR, exist_ok=True)

# ---------------------------
# 1. 전체 글 가져오기 (skip 방식)
# ---------------------------
def get_all_posts():
    url = "https://v2.velog.io/graphql"
    all_posts = []
    skip = 0
    LIMIT = 20

    while True:
        query = """
        query Posts($username: String!, $limit: Int!, $skip: Int!) {
          posts(username: $username, limit: $limit, skip: $skip) {
            id
            title
            released_at
            url_slug
          }
        }
        """

        res = requests.post(url, json={
            "query": query,
            "variables": {
                "username": USERNAME,
                "limit": LIMIT,
                "skip": skip
            }
        }).json()

        posts = res["data"]["posts"]

        if not posts:
            break

        all_posts.extend(posts)
        skip += LIMIT

        print(f"Loaded {len(all_posts)} posts...")
        time.sleep(0.3)  # rate limit 방지

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

    res = requests.post(url, json={
        "query": query,
        "variables": {
            "username": USERNAME,
            "url_slug": slug
        }
    }).json()

    return res["data"]["post"]


# ---------------------------
# 3. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 4. 이미지 다운로드 + 경로 변경
# ---------------------------
def process_images(html, img_dir):
    soup = BeautifulSoup(html, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        try:
            filename = src.split("/")[-1].split("?")[0]
            filepath = os.path.join(img_dir, filename)

            # 이미 있으면 다운로드 안 함 (최적화)
            if not os.path.exists(filepath):
                img_data = requests.get(src, timeout=10).content
                with open(filepath, "wb") as f:
                    f.write(img_data)

            img["src"] = f"./images/{filename}"

        except Exception as e:
            print("Image error:", e)

    return str(soup)


# ---------------------------
# 5. 메인 로직
# ---------------------------
def main():
    posts = get_all_posts()

    for post in posts:
        slug = post["url_slug"]

        try:
            detail = get_post_detail(slug)
        except:
            print(f"Skip (detail fail): {slug}")
            continue

        if not detail:
            continue

        title = detail["title"]
        body = detail["body"]

        date = datetime.fromisoformat(
            detail["released_at"].replace("Z", "")
        )

        year = str(date.year)
        month = str(date.month).zfill(2)
        date_prefix = date.strftime("%Y-%m-%d")

        # 폴더 생성
        post_dir = os.path.join(BASE_DIR, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date_prefix}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # 이미 있으면 skip (속도 최적화)
        if os.path.exists(file_path):
            continue

        # 이미지 폴더
        img_dir = os.path.join(post_dir, "images")
        os.makedirs(img_dir, exist_ok=True)

        # 이미지 처리
        body = process_images(body, img_dir)

        markdown = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%d %H:%M:%S')}
---

{body}
"""

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved: {file_name}")


if __name__ == "__main__":
    main()
