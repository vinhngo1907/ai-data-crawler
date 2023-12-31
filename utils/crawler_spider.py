import requests, re, random, datetime as dt
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from twitterscraper import query_tweets
from ast import literal_eval

# api_key = "AIzaSyA-xf1iJjNQCELDVGDtYJ7aM0t1ZulB0kQ"
api_key = "AIzaSyCuJiO5AOoeVIyYY0k0fd5Jzjk4gYSFWug"
cse_id = "016133495723645302024:cfibqauizrm"


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


def social_media_scrape():
    """
    :param query:
    :param keywords:
    :return: crawled links, scrape data
    """
    general = list()
    crime = list()
    
    return True
