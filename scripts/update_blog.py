import feedparser
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


# ---------------------------
# 1. RSS 페이지네이션으로 전체 글 가져오기
# ---------------------------
def get_all_posts():
    all_entries = []
    page = 1

    while True:
        url = f'https://api.velog.io/rss/@{USERNAME}?page={page}'
        print(f"Fetching page {page}: {url}")

        feed = feedparser.parse(url)

        if not feed.entries:
            print(f"No more entries at page {page}. Done.")
            break

        # 이전 페이지와 중복이면 종료
        existing_links = {e.link for e in all_entries}
        new_entries = [e for e in feed.entries if e.link not in existing_links]

        if not new_entries:
            print(f"Duplicate entries at page {page}. Done.")
            break

        all_entries.extend(new_entries)
        print(f"Loaded {len(all_entries)} posts so far...")

        # 한 페이지가 20개 미만이면 마지막 페이지
        if len(feed.entries) < 20:
            break

        page += 1
        time.sleep(0.5)

    return all_entries


# ---------------------------
# 2. 파일명 정리
# ---------------------------
def sanitize(text):
    return re.sub(r'[\\/*?:"<>|]', '-', text)


# ---------------------------
# 3. 날짜 파싱
# ---------------------------
def parse_date(entry):
    try:
        return datetime(*entry.published_parsed[:6])
    except:
        return datetime.now()


# ---------------------------
# 4. 메인 로직
# ---------------------------
def main():
    entries = get_all_posts()
    print(f"\nTotal posts: {len(entries)}")

    if not entries:
        print("No posts fetched. Exiting.")
        return

    changed = False

    for entry in entries:
        title = entry.title
        link = entry.link
        date = parse_date(entry)

        year = str(date.year)
        month = str(date.month).zfill(2)

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

        time.sleep(0.3)

    if changed:
        repo.git.push()
        print("Pushed to GitHub.")
    else:
        print("No changes to push.")


if __name__ == "__main__":
    main()
