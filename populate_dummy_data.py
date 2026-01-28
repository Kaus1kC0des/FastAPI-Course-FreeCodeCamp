import time
import random
import requests

response = requests.get("https://jsonfakery.com/blogs").json()
published_options = [True, False]

times = []

for post in response:
    payload = {
        "title": post.get("title"),
        "content": post.get("main_content"),
        "published": random.choice(published_options),
    }

    start = time.perf_counter()
    r = requests.post("http://localhost:8000/posts", json=payload)
    end = time.perf_counter()

    times.append(end - start)

avg = sum(times) / len(times)

print(f"Total requests: {len(times)}")
print(f"Average response time: {avg * 1000:.2f} ms")
print(f"Min: {min(times)*1000:.2f} ms")
print(f"Max: {max(times)*1000:.2f} ms")
