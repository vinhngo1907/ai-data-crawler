import requests, re, random, datetime as dt
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# from twitterscraper import query_tweets
from ast import literal_eval

api_key = ""
cse_id = ""


def google_query(query, **kwargs):
    """
    :param query:
    :param kwargs:
    :return: scrape data
    """
    query_service = build("customsearch", "v1", developerKey=api_key)
    query_results = query_service.cse().list(q=query, cx=cse_id, **kwargs).execute()

    try:
        return query_results["items"]
    except:
        return dict()


keywords = ["Crime", "Child Abuse", "Women Abuse", "Cyber Bullying"]

# def crawling(query, keyword):
#     """
#     :param query:
#     :param keywords:
#     :return: crawled links, scrape data
#     """
#     general = list()
#     crime = list()
#     child_abuse = list()
#     women_abuse = list()
#     pornography = list()
#     rape = list()
#     cyber_bullying = list()
#     general_scrape = list()
#     crime_scrape = list()
#     child_abuse_scrape = list()
#     women_abuse_scrape = list()
#     pornography_scrape = list()
#     rape_scrape = list()
#     cyber_bullying_scrape = list()

#     contenxt = {
#         "general": general,
#         "crime": crime,
#         "child abuse": child_abuse,
#         "woman abuse": women_abuse,
#         "cyber_bullying": cyber_bullying,
#     }
#     reduced = [
#         general[:4],
#         crime[:4],
#         child_abuse[:4],
#         women_abuse[:4],
#         cyber_bullying[:4],
#     ]

#     reduced2 = [
#         general_scrape[:4],
#         crime_scrape[:4],
#         child_abuse_scrape[:4],
#         women_abuse_scrape[:4],
#         cyber_bullying_scrape[:4],
#     ]


def scraper(link):
    """

    :param link:
    :return: scrape data
    """
    print(f"scraping {link}")
    if "youtube" in str(link):
        return {}
    else:
        page = requests.get(str(link))
        soup = BeautifulSoup(page.content, "html.parser")
        metadata = dict()
        for tag in soup.find_all("meta"):
            name = tag.attrs.get("name")
            property = tag.attrs.get("property")
            content = tag.attrs.get("content")
            if name or property:
                if name:
                    if ":":
                        names = name.split(":")
                        name = names[1]
                    metadata[name] = content
                else:
                    if ":" in property:
                        props = property.split(":")
                        property = props[1]
                    metadata[property] = content
        print(metadata)
        return metadata


# def social_media_scrape(keyword):
#     result = {}
#     temp = {}
#     base_url = "twitter.com"
#     query = str(keyword) + " " + keywords[0]
#     tweets = query_tweets(query, limit=1, begindate=dt.date(2023, 6, 21), proxy=None)
#     return tweets


def extract_image(data):
    print("exttracting images", data)
    try:
        image = data["pagemap"]["metatags"][0]["og:image"]
        return image
    except:
        pass


def create_predict_image(images, images_list):
    context = dict()
    for image in images:
        for image_list in images_list:
            context[image] = image_list

    return context
