from bs4 import BeautifulSoup
import requests
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_api.settings")
import django
django.setup()
from news.models import News


BASE_URL = "https://sports.news.naver.com/index"
HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}


def get_news():
    res = requests.get(BASE_URL, headers=HEADER)
    soup = BeautifulSoup(res.text, "html.parser")

    data = soup.select(".today_item")
    result = []

    for i in data:
        news_obj = {
            'title': i.select('a > div.text_area > strong')[0].text,
            'url': BASE_URL + i.find("a")["href"],
            'press': i.find_all(class_="information")[0].find_all('span')[0].text,
            'category': i.find_all(class_="information")[0].find_all('span')[1].text
        }
        result.append(news_obj)

    return result


if __name__=='__main__':
    data = get_news()
    print(data)
    for item in data:
        News(title=item['title'], url=item['url'], press=item['press'], category=item['category']).save()
