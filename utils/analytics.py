from crawler.models import Link, Category, UserProfile, CrawledLinks
from pytrends.request import TrendReq
import random


def category_count(user):
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


def category_percent(user):
    temp = category_count(user)
    total = sum(temp)
    percent = list()
    context = dict()

    for item in temp:
        if total != 0:
            percent.append((item / total) * 100)

    categories = Category.objects.all()
    for category, p in zip(categories, percent):
        context[category.name] = round(p, 2)

    return context


def keyword_trends(keyword_list):
    context = dict()
    temp = list()
    try:
        print("Hello")
        pytrend = TrendReq(timeout=(10, 25), backoff_factor=0.5)

        def color():
            return random.randint(0, 255)

        pytrend.build_payload(kw_list=keyword_list)
        interest_over_time_df = pytrend.interest_over_time()
        labels = interest_over_time_df.index.tolist()
        for item in labels:
            temp.append(str(item))

        for keyword in keyword_list:
            context[keyword] = interest_over_time_df[keyword].tolist(), (
                "#%02X%02X%02X" % (color(), color(), color())
            )
    except:
        print(" No Trends")

    return temp, context
