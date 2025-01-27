
url = 'https://www.reuters.com/technology/chinas-deepseek-sets-off-ai-market-rout-2025-01-27/'
from bs4 import BeautifulSoup
import requests

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

title = soup.find("title").get_text()  # Extract title
meta_author = soup.find("meta", {"name": "author"})
author = meta_author["content"] if meta_author else "Author not found"
meta_date = soup.find("meta", {"property": "article:published_time"})
date = meta_date["content"] if meta_date else "Date not found"

print("Title:", title)
print("Author:", author)
print("Publication Date:", date)
print("Source:", url)

