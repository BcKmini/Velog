import os
import requests
import json

API_KEY = os.environ['VELOG_API_KEY']
BASE_URL = 'https://v2.velog.io/api'

def get_posts():
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(f'{BASE_URL}/posts', headers=headers)
    return response.json()

def save_post(post):
    title = post['title']
    content = post['body']
    filename = f"posts/{title.replace(' ', '_')}.md"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n{content}")

posts = get_posts()
for post in posts:
    save_post(post)
