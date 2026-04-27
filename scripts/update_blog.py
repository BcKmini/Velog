import requests
import os
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup

USERNAME = "mi_nini"
BASE_DIR = "velog-posts"

os.makedirs(BASE_DIR, exist_ok=True)

# ---------------------------
# 1. Velog GraphQL로 전체 글 가져오기
# ---------------------------
def get_all_posts():
    url = "https://v2.velog.io/graphql"

    query = """
    query Posts($username: String!) {
      posts(username: $username) {
        id
        title
        short_description
        released_at
        url_slug
      }
    }
    """

    res = requests.post(url, json={
        "query": query,
        "variables": {"username": USERNAME}
    })

    return res.json()["data"]["posts"]


# ---------------------------
# 2. 개별 글 상세 가져오기
# ---------------------------
def get_post_detail(url_slug):
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
            "url_slug": url_slug
        }
    })

    return res.json()["data"]["post"]


# ---------------------------
# 3. 이미지 다운로드
# ---------------------------
def download_images(html, img_dir):
    soup = BeautifulSoup(html, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        try:
            filename = src.split("/")[-1].split("?")[0]
            filepath = os.path.join(img_dir, filename)

            if not os.path.exists(filepath):
                img_data = requests.get(src).content
                with open(filepath, "wb") as f:
                    f.write(img_data)

            # 👉 경로 로컬로 치환
            img["src"] = f"./images/{filename}"

        except Exception as e:
            print("Image download failed:", e)

    return str(soup)


# ---------------------------
# 4. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 5. 전체 실행
# ---------------------------
def main():
    posts = get_all_posts()

    for post in posts:
        slug = post["url_slug"]
        detail = get_post_detail(slug)

        title = detail["title"]
        body = detail["body"]
        date = datetime.fromisoformat(detail["released_at"].replace("Z", ""))

        year = str(date.year)
        month = str(date.month).zfill(2)
        date_prefix = date.strftime("%Y-%m-%d")

        # 폴더 생성
        post_dir = os.path.join(BASE_DIR, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date_prefix}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # 이미지 폴더
        img_dir = os.path.join(post_dir, "images")
        os.makedirs(img_dir, exist_ok=True)

        # 이미지 다운로드 + HTML 수정
        body = download_images(body, img_dir)

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
