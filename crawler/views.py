from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Category, CrawledLinks
from scheduler.models import ScrapedLink
from django.db.models import Count
from django.contrib import messages
from utils.analytics import category_percent, category_count, keyword_trends
import random, json, copy


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
