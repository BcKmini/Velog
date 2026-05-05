import feedparser
import git
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

USERNAME = "mi_nini"
rss_url = f'https://api.velog.io/rss/@{USERNAME}'

repo_path = '.'
BASE_DIR = "velog-posts"
posts_dir = os.path.join(repo_path, BASE_DIR)
os.makedirs(posts_dir, exist_ok=True)

repo = git.Repo(repo_path)


# ---------------------------
# 1. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 2. 날짜 파싱
# ---------------------------
def parse_date(entry):
    try:
        return datetime(*entry.published_parsed[:6])
    except:
        return datetime.now()


# ---------------------------
# 3. 메인 로직
# ---------------------------
def main():
    feed = feedparser.parse(rss_url)
    print(f"RSS URL: {rss_url}")
    print(f"Total posts: {len(feed.entries)}")

    if not feed.entries:
        print("No posts fetched. Exiting.")
        return

    changed = False

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        date = parse_date(entry)

        year = str(date.year)
        month = str(date.month).zfill(2)

        # 연도/월 폴더 구분
        post_dir = os.path.join(posts_dir, year, month)
        os.makedirs(post_dir, exist_ok=True)

        safe_title = sanitize(title)
        file_name = f"{date.strftime('%Y-%m-%d')}_{safe_title}.md"
        file_path = os.path.join(post_dir, file_name)

        # HTML → 텍스트 변환
        soup = BeautifulSoup(entry.description, "html.parser")
        body = soup.get_text(separator="\n").strip()

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

    if changed:
        repo.git.push()
        print("Pushed to GitHub.")
    else:
        print("No changes to push.")


if __name__ == "__main__":
    main()
