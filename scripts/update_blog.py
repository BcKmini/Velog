import feedparser
import git
import os
import requests
from bs4 import BeautifulSoup
import re

# Velog RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@mi_nini'

# GitHub 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 파일 이름 생성
    file_name = re.sub(r'[^\w\-_\. ]', '_', entry.title)
    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # Velog 포스트 전체 내용 가져오기
    response = requests.get(entry.link)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', class_='velog-content')

    if content:
        # 파일 생성 또는 업데이트
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {entry.title}\n\n")
            file.write(f"작성일: {entry.published}\n\n")
            file.write(content.get_text())

        # 변경사항이 있으면 커밋
        if repo.is_dirty(path=file_path):
            repo.git.add(file_path)
            repo.git.commit('-m', f'Update post: {entry.title}')
            print(f"커밋됨: {entry.title}")
        else:
            print(f"변경사항 없음: {entry.title}")

# 변경 사항을 GitHub에 푸시
repo.git.push()
print("모든 변경사항이 GitHub에 푸시되었습니다.")
