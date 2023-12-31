from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Category, CrawledLinks
from scheduler.models import ScrapedLink
from django.db.models import Count
from django.contrib import messages
from utils.analytics import category_percent, category_count, keyword_trends
import random, json, copy
from utils.crawler_spider import social_media_scrape



@login_required
def index(request):
    """ """
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    category = Category.objects.all()
    notifications = Notifications.objects.filter(user=userprofile).order_by("-pub_date")
    unread = notifications.filter(read=False)
    user_crawled_links = CrawledLinks.objects.filter(userprofile=userprofile).order_by(
        "-pub_date"
    )
    context = dict()
    context["home"] = True
    context["category"] = category
    context["userprofile"] = userprofile
    context["notifications"] = notifications[:5]
    context["unread_count"] = len(unread)
    context["user_crawled"] = user_crawled_links[: userprofile.recent_link]
    context["cat_percent"] = category_percent(request.user)

    return render(request, "crawler/index.html", context=context)


@login_required
def crawler_index(request):
    context = dict()
    userprofile = UserProfile.objects.get_or_create(user=request.user)
    notifications = Notifications.objects.filter(user=userprofile).order_by("-pub_date")
    unread = notifications.filter(read=False)
    categories = [i.name for i in Category.objects.all()]
    crawled_links = CrawledLinks.objects.order_by("-pub_date")
    user_crawled_links = CrawledLinks.objects.filter(userprofile=userprofile).order_by(
        "-pub_date"
    )
    unique_keyword = list(
        crawled_links.filter(userprofile=userprofile)
        .order_by()
        .values_list("link__keyword__name", flat=True)
        .distinct()
    )
    copy_keyword = copy.copy(unique_keyword)
    random.shuffle(copy_keyword)

    keyword_labels, keywords_dataset = keyword_trends(copy_keyword[1:6])
    print(category_count(request.user))

    context["crawler_home"] = True
    context["userprofile"] = userprofile
    context["notifications"] = notifications[:5]
    context["unread_count"] = len(unread)
    context["crawler_links"] = crawled_links
    context["categories"] = categories
    context["unique_keyword"] = unique_keyword
    context["keyword_labels"] = keyword_labels
    context["keyword_dataset"] = keywords_dataset

    return render(request, "crawler/crawler.html", context=context)


@login_required
def report(request):
    """
    :param request:
    :return: Detail Report
    """

    context = dict()
    render_dict = dict()
    temp = dict()
    category = Category.objects.all()
    userprofile = UserProfile.objects.get(user=request.user)
    notifications = Notifications.objects.filter(user=userprofile)
    unread = notifications.filter(read=False)
    categories = [i.name for i in Category.objects.all()]
    crawled_links = CrawledLinks.objects.filter(user=userprofile)
    unique_keywords = list(
        crawled_links.values_list("link__keyword__name", flat=True).distinct()
    )
    for keyword in unique_keywords:
        for category in categories:
            temp[category] = CrawledLinks.objects.filter(
                userprofile=userprofile,
                link__keyword__name=keyword,
                link__category__name=category,
            )
        context[keyword] = temp

    print(context)
    render_dict["report"] = True
    render_dict["category"] = category
    render_dict["userprofile"] = userprofile
    render_dict["notifications"] = notifications[:5]
    render_dict["unread_count"] = len(unread)
    render_dict["data"] = context
    return render(request, "crawler/report.html", context=render_dict)


@login_required
def social(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
        scrape_data = social_media_scrape(keyword)
        context = {"scrape_data": scrape_data}
        return render(None, "crawler/sociale.html", context=context)
