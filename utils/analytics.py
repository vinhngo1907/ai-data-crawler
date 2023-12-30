from crawler.models import Link, Category, UserProfile, CrawledLinks
from pytrends.request import TrendReq
import random


def category_percent(user):
    temp = list()
    categories = Category.objects.all()
    userprofile = UserProfile.objects.get(user=user)

    for category in categories:
        links = len(
            CrawledLinks.objects.filter(
                userprofile=userprofile, link__category__name=category.name
            )
        )

        temp.append(links)
    return temp