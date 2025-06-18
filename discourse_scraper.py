
import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in/"
CATEGORY = "c/tools-in-data-science"

def scrape_posts():
    posts = []
    for page in range(1, 6):
        url = f"{BASE_URL}{CATEGORY}?page={page}"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        topics = soup.find_all('a', class_='title raw-link raw-topic-link')
        for topic in topics:
            link = BASE_URL + topic['href']
            title = topic.get_text(strip=True)
            posts.append({"title": title, "url": link})

    with open("data/discourse_data.json", "w") as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    scrape_posts()
