import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

os.chdir(os.getcwd() + r"/data")  # csv 파일 저장 경로

BASE_URL = "https://search.naver.com/search.naver?"
COMMENT_URL = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=view_it&pool=cbox5&_wr&_callback=jQuery112401841839960753442_1630905379082&lang=ko&country=KR&categoryId=&pageSize=10&indexSize=10&groupId=&listType=OBJECT&pageType=more&refresh=true&sort=FAVORITE&moreParam.direction=next&moreParam.prev=00000100000200000018au5fa&moreParam.next=0000-500000200000018asya8&includeAllStatus=true&_=1630905379085"
REACTION_URL = "https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery112407839462533429615_1630909363366&isDuplication=false&_=1630909363367&"
HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}


def scraper(query):
    urls = []
    for page in range(10):
        res = requests.get(BASE_URL + "query=" + query + "&where=news&ie=utf8&sm=nws_hty" + "&start=" + str(page*10 + 1), headers=HEADER)
        soup = BeautifulSoup(res.text, "html.parser")

        select = soup.find_all(class_="info_group")

        for i in select:
            try:
                url = i.find_all("a")[1]["href"]
                urls.append(url)
            except IndexError:      # 네이버뉴스가 존재하지 않을 경우
                pass
    result = []

    for url in urls:
        print(url)
        res = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(res.text, "html.parser")
        oid = url.split("oid=")[1].split("&")[0]
        aid = url.split("aid=")[1]
        parm = oid + "_" + aid
        page = 1

        news = {}
        try:
            news["title"] = soup.find(id="articleTitle").text
        except AttributeError:      # 네이버 연애 뉴스로 접근했을 경우 형식이 달라서 제외
            continue

        news["body"] = soup.find(id="articleBodyContents").text.strip()

        try:
            news["press"] = soup.find(class_="journalistcard_summary_press").find("img")["alt"]
        except AttributeError:      # 언론사가 위치한 곳에 없을 경우 로고 이미지로 접근해서 가져옴
            news["press"] = soup.find(class_="press_logo").find("img")["title"]

        try:
            news["journalist"] = soup.find(class_="journalistcard_summary_name").text
        except AttributeError:      # 기자 이름이 위치한 곳에 없을 경우
            news["journalist"] = soup.find(class_="b_text").text.strip()

        header = HEADER
        header["referer"] = url
        c_url = COMMENT_URL + "&objectId=news" + oid + "%2C" + aid + "&page=" + str(page)
        comment_res = requests.get(c_url, headers=HEADER)

        comment = comment_res.text.replace("jQuery112401841839960753442_1630905379082(", "").replace(");", "")
        comment = comment.replace("true", "True").replace("null", "None").replace("false", "False")
        comment = eval(comment)
        news["comment_num"] = comment["result"]["count"]["comment"]

        r_url = REACTION_URL + "q=NEWS%5Bne_" + parm + "%5D%7CNEWS_SUMMARY%5B" + parm + "%5D%7CJOURNALIST%5B56635(period)%5D%7CNEWS_MAIN%5Bne_" + parm + "%5D"
        reaction_res = requests.get(r_url, headers=HEADER)

        reaction = reaction_res.text.replace("/**/jQuery112407839462533429615_1630909363366(", "").replace(");", "")
        reaction = reaction.replace("true", "True").replace("null", "None").replace("false", "False")
        reaction = eval(reaction)

        news["angry"] = "0"
        news["warm"] = "0"
        news["like"] = "0"
        news["want"] = "0"
        news["sad"] = "0"

        for i in reaction["contents"][0]["reactionMap"]:
            reaction_name = reaction["contents"][0]["reactionMap"][i]["reactionTypeCode"]["name"]
            reaction_num = reaction["contents"][0]["reactionMap"][i]["count"]
            news[reaction_name] = reaction_num

        now = time.localtime()
        news["time"] = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        result.append(news)
        df = pd.DataFrame(result)
        title = query + "_news.csv"
        df.to_csv(title, sep=",", index=True, encoding="utf-8-sig")


if __name__ == '__main__':
    query = input()
    scraper(query)
