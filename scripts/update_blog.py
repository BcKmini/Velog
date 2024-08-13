import feedparser
import git
import os
import re
from datetime import datetime

# 벨로그 RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@mi_nini'
repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

repo = git.Repo(repo_path)

def clean_filename(title):
    # 파일명에서 사용할 수 없는 문자 제거 및 대체
    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
    clean_title = clean_title.replace(' ', '_')
    return clean_title[:100]  # 파일명 길이 제한

def get_full_content(entry):
    return entry.content[0].value if 'content' in entry else entry.description

try:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        file_name = clean_filename(entry.title) + '.md'
        file_path = os.path.join(posts_dir, file_name)
        
        content = f"""---
title: {entry.title}
date: {datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M:%S")}
url: {entry.link}
---

{get_full_content(entry)}
"""
        
        if not os.path.exists(file_path) or open(file_path, 'r', encoding='utf-8').read() != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            repo.git.add(file_path)
            repo.git.commit('-m', f'Add/Update post: {entry.title}')
            print(f"Added/Updated: {entry.title}")
        else:
            print(f"No changes: {entry.title}")

    if repo.is_dirty():
        repo.git.push()
        print("Changes pushed to remote repository")
    else:
        print("No changes to push")

except Exception as e:
    print(f"An error occurred: {str(e)}")
