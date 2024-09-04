import feedparser
import git
import os

# 벨로그 RSS 피드 URL
rss_url = 'https://api.velog.io/rss/@mi_nini'

# 깃허브 레포지토리 경로
repo_path = '.'

# 'velog-posts' 폴더 경로
posts_dir = os.path.join(repo_path, 'velog-posts')

# 'velog-posts' 폴더가 없다면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# 원격 저장소의 변경 사항을 로컬로 가져오기
try:
    repo.git.pull('origin', 'main')
except git.exc.GitCommandError as e:
    print(f"Failed to pull from remote: {e}")

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 이미 커밋된 파일 목록 가져오기
committed_files = set()
for commit in repo.iter_commits('--all'):
    committed_files.update(commit.stats.files.keys())

# 각 글을 파일로 저장하고 커밋
for entry in feed.entries:
    # 시리즈 이름 가져오기 (시리즈가 없는 경우 기본 폴더에 저장)
    series_name = entry.get('tags', [{'term': '3-2'}])[0]['term']  # 시리즈명이 없으면 'default' 폴더에 저장

    # 시리즈 폴더 경로
    series_dir = os.path.join(posts_dir, series_name)

    # 시리즈 폴더가 없다면 생성
    if not os.path.exists(series_dir):
        os.makedirs(series_dir)

    # 파일 이름에서 유효하지 않은 문자 제거 또는 대체
    file_name = entry.title
    file_name = file_name.replace('/', '-')  # 슬래시를 대시로 대체
    file_name = file_name.replace('\\', '-')  # 백슬래시를 대시로 대체
    # 필요에 따라 추가 문자 대체
    file_name += '.md'

    # 파일 경로
    file_path = os.path.join(series_dir, file_name)

    # 파일이 이미 존재하지 않으며, 다른 시리즈에 커밋되지 않은 경우에만 생성
    if file_path not in committed_files and not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(entry.description)  # 글 내용을 파일에 작성

        # 깃허브 커밋
        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title} to series: {series_name}')

# 변경 사항을 깃허브에 푸시
try:
    repo.git.push('origin', 'main')
except git.exc.GitCommandError as e:
    print(f"Failed to push to remote: {e}")
