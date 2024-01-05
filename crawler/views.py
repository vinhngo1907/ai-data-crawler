from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Category, CrawledLinks, Keyword
from scheduler.models import ScrapedLink
from django.db.models import Count
from django.contrib import messages
from utils.analytics import category_percent, category_count, keyword_trends

# from utils.crawler_spider import social_media_scrape
from utils.news import news
import random, json, copy
from django.http import JsonResponse


@login_required
def index(request):
    """
    :param request:
    :return: Home Page
    """
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
    # return HttpResponse(context)


@login_required
def crawler_index(request):
    """
    :param request:
    :return: Crawler Page
    """

    context = dict()
    userprofile = UserProfile.objects.get(user=request.user)
    notifications = Notifications.objects.filter(user=userprofile).order_by("-pub_date")
    unread = notifications.filter(read=False)
    categories = [i.name for i in Category.objects.all()]
    crawled_links = CrawledLinks.objects.order_by("-pub_date")

    unique_keyword = list(
        crawled_links.filter(userprofile=userprofile)
        .order_by()
        .values_list("link__keyword__name", flat=True)
        .distinct()
    )
    copy_keyword = copy.copy(unique_keyword)
    random.shuffle(copy_keyword)

    keyword_labels, keywords_dataset = keyword_trends(copy_keyword[1:6])

    context["crawler_home"] = True
    context["userprofile"] = userprofile
    context["notifications"] = notifications[:5]
    context["unread_count"] = len(unread)
    context["crawler_links"] = crawled_links
    context["categories"] = categories
    context["category_data"] = category_count(request.user)
    context["unique_keyword"] = unique_keyword
    context["keywords_labels"] = keyword_labels
    context["keywords_dataset"] = keywords_dataset

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
    
    notifications = Notifications.objects.filter(user=userprofile).order_by("-pub_date")
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


# @login_required
# def social(request):
#     if request.method == "POST":
#         keyword = request.POST.get("keyword")
#         scrape_data = social_media_scrape(keyword)
#         context = {"scrape_data": scrape_data}
#         return render(None, "crawler/social.html", context=context)


@login_required
def test(request):
    """

    :param request:
    :return: Beta Testing
    """
    userprofile = UserProfile.objects.filter(user=request.user)[0]
    context = dict()
    context["userprofile"] = userprofile
    return render(request, "crawler/result.html", context)


@login_required
def calendar(request, keyword):
    """

    :param request:
    :param keyword:
    :return: Falcon Custom API
    """
    temp = dict()
    result = news(keyword)
    userprofile = UserProfile.objects.filter(user=request.user)[0]
    key = Keyword.objects.get(name=keyword)
    crawled_links = CrawledLinks.objects.filter(
        userprofile=userprofile, link__keyword=key
    )

    for link in crawled_links:
        temp[link.link.link] = link.link.scrape_data

    temp["summarized data"] = result
    data = {keyword: temp}

    return JsonResponse(data)


@login_required
def process(request):
    """
    :param request:
    :return: Result page
    """
    if request.method == "POST":
        userprofile = UserProfile.objects.get(user=request.user)[0]
        notifications = Notifications.objects.filter(user=userprofile).order_by(
            "-pub_date"
        )
        unread = notifications.filter(read=False)
        main_search = request.POST.get("main_search")

        context = dict()
        context["userprofile"] = userprofile
        context["notifications"] = notifications[:5]
        context["unread"] = len(unread)

        return render(None, "crawler/process.html", context=context)
