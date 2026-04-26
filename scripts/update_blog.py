import feedparser
import git
import os
import json
import re
from datetime import datetime

rss_url = 'https://api.velog.io/rss/@mi_nini'
repo_path = '.'

base_dir = os.path.join(repo_path, 'velog-posts')
index_file = os.path.join(base_dir, 'post_index.json')

repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

# 폴더 생성
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# 인덱스 로드
if os.path.exists(index_file):
    with open(index_file, 'r', encoding='utf-8') as f:
        post_index = json.load(f)
else:
    post_index = {}

new_posts = False

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', '-', name)
    name = name.strip()
    return name

for entry in feed.entries:
    post_id = entry.link

    if post_id in post_index:
        print(f"Skip: {entry.title}")
        continue

    # 날짜 처리
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6])
    else:
        dt = datetime.now()

    year = str(dt.year)
    month = str(dt.month).zfill(2)
    date_prefix = dt.strftime('%Y-%m-%d')

    # 폴더 생성 (YYYY/MM)
    target_dir = os.path.join(base_dir, year, month)
    os.makedirs(target_dir, exist_ok=True)

    # 파일명 (정렬 고려)
    safe_title = sanitize_filename(entry.title)
    file_name = f"{date_prefix}_{safe_title}.md"
    file_path = os.path.join(target_dir, file_name)

    # 본문 (간단 markdown 형태)
    content = f"""---
title: "{entry.title}"
date: {dt.strftime('%Y-%m-%d %H:%M:%S')}
link: {entry.link}
---

{entry.description}
"""

    # 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 인덱스 업데이트
    post_index[post_id] = file_path

    repo.git.add(file_path)
    print(f"Added: {file_name}")
    new_posts = True

# 인덱스 커밋
if new_posts:
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(post_index, f, indent=2, ensure_ascii=False)

    repo.git.add(index_file)
    repo.git.commit('-m', f'Auto sync velog posts ({datetime.now().strftime("%Y-%m-%d %H:%M")})')
    repo.git.push()
else:
    print("No new posts.")
