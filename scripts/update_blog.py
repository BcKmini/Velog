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
readme_path = os.path.join(repo_path, 'README.md')

repo = git.Repo(repo_path)
feed = feedparser.parse(rss_url)

os.makedirs(base_dir, exist_ok=True)

# 인덱스 로드
if os.path.exists(index_file):
    with open(index_file, 'r', encoding='utf-8') as f:
        post_index = json.load(f)
else:
    post_index = {}

new_posts = False

def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', '-', name)
    return name.strip()

def update_readme(feed):
    if not os.path.exists(readme_path):
        return

    posts = feed.entries[:3]

    new_content = ""
    for post in posts:
        title = post.title
        link = post.link

        if hasattr(post, 'published_parsed') and post.published_parsed:
            dt = datetime(*post.published_parsed[:6])
            date_str = dt.strftime('%Y-%m-%d')
        else:
            date_str = "unknown"

        new_content += f"- [{title}]({link}) ({date_str})\n"

    new_content += f"\n[Velog에서 더 보기](https://velog.io/@mi_nini)\n"

    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    start_tag = "<!-- BLOG-POST-LIST:START -->"
    end_tag = "<!-- BLOG-POST-LIST:END -->"

    start = content.find(start_tag)
    end = content.find(end_tag)

    if start == -1 or end == -1:
        print("README tag not found")
        return

    updated = (
        content[:start + len(start_tag)] +
        "\n" + new_content +
        content[end:]
    )

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated)

    repo.git.add(readme_path)

for entry in feed.entries:
    post_id = entry.link

    if post_id in post_index:
        continue

    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6])
    else:
        dt = datetime.now()

    year = str(dt.year)
    month = str(dt.month).zfill(2)
    date_prefix = dt.strftime('%Y-%m-%d')

    target_dir = os.path.join(base_dir, year, month)
    os.makedirs(target_dir, exist_ok=True)

    safe_title = sanitize_filename(entry.title)
    file_name = f"{date_prefix}_{safe_title}.md"
    file_path = os.path.join(target_dir, file_name)

    content = f"""---
title: "{entry.title}"
date: {dt.strftime('%Y-%m-%d %H:%M:%S')}
link: {entry.link}
---

{entry.description}
"""

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    post_index[post_id] = file_path
    repo.git.add(file_path)
    new_posts = True

# 커밋 처리
if new_posts:
    # README 업데이트
    update_readme(feed)

    # 인덱스 저장
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(post_index, f, indent=2, ensure_ascii=False)

    repo.git.add(index_file)

    repo.git.commit('-m', f'Auto sync velog posts ({datetime.now().strftime("%Y-%m-%d %H:%M")})')
    repo.git.push()
else:
    print("No new posts.")
