import requests
import random
import json
import html
from sqlalchemy import select
from app.database import SyncSessionLocal

# Import all models to ensure relationships are properly configured
from app.models.users import Users
from app.models.auth_details import UserAuth
from app.models.posts import Posts
from app.models.tags import Tags
from app.models.post_tags import PostTags
from app.models.post_metrics import PostMetrics

TAGS_URL = "https://dummyjson.com/posts?limit=1000"
tags = set()

tags_data = requests.get(TAGS_URL).json().get("posts")

for i in tags_data:
    for tag in i.get("tags"):
        tags.add(tag.lower())
tags = list(tags)

# Fetch user IDs from database
with SyncSessionLocal() as db:
    result = db.execute(select(Users.id))
    user_ids = [row[0] for row in result.fetchall()]

if not user_ids:
    print("No users found in database. Please populate users first.")
    exit(1)

print(f"Found {len(user_ids)} users in database")

POSTS_URL = "https://jsonfakery.com/blogs"
posts = requests.get("https://jsonfakery.com/blogs").json()

for post in posts:
    total_tags_random = random.randint(2, min(4, len(tags)))
    total_users = len(user_ids)
    random_likes = random.randint(0, total_users)
    random_dislikes = random.randint(0, total_users - random_likes)
    payload = {
        "title": post.get("title"),
        "body": html.unescape(post.get("main_content")),
        "tags": random.sample(tags, total_tags_random),
        "reactions": {"likes": random_likes, "dislikes": random_dislikes},
        "views": random.randint(50, 1000),
        "userId": random.choice(user_ids),
    }
    response = requests.post("http://localhost:8000/posts/ingest", json=payload)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        break
    print(response)
