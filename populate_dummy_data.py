import requests
import time
import random
import requests

BASE_URL = "https://dummyjson.com/users/"

for i in range(1, 209):
    url = BASE_URL + str(i)
    user = requests.get(url).json()
    user["confirm_password"] = user.get("password")
    response = requests.post("http://localhost:8000/users/create", json=user)
    print(response)
