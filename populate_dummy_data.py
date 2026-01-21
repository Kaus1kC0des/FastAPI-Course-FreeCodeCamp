from random import random
import requests
import random

response = requests.get("https://jsonfakery.com/blogs").json()
published_options = [True, False]

for post in response:
    payload = {
        "title": post.get("title"),
        "content": post.get("main_content"),
        "published": random.choice(published_options),
    }
    requests.post("http://localhost:8000/posts", json=payload)
