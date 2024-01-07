from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Category, CrawledLinks, Keyword
from crawler.tasks import save_models
from scheduler.models import ScrapedLink
from django.db.models import Count
from django.contrib import messages
from utils.analytics import category_percent, category_count, keyword_trends
from utils.image_processing import category_predict
from utils.crawler_spider import (
    social_media_scrape,
    crawling,
    extract_images,
    wiki_scraping,
    count_items
)
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

    crawled_links = CrawledLinks.objects.filter(userprofile=userprofile).order_by(
        "pub_date"
    )
    categories = [i.name for i in Category.objects.all()]

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
def calendar(request):
    context = dict()
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    categories = Category.objects.all()
    notifications = Notifications.objects.filter(user=userprofile).order_by("-pub_date")
    unread = notifications.filter(read=False)
    context["calendar"] = True
    context["category"] = categories
    context["userprofile"] = userprofile
    context["notifications"] = notifications[:5]
    context["unread"] = len(unread)

    return render(request, "crawler/calendar.html", context)


@login_required
def api(request, keyword):
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
        filters = request.POST["multiple_select"]
        reschedule_crawler = request.POST.get("reschedule_crawler")
        print(type(main_search), type(filters))

        main_search_list = [x.strip(" ") for x in main_search.split(",")]
        filters_list = [x.strip(" ") for x in filters.split(",")]

        result1 = dict()
        result2 = dict()
        result3 = dict()
        result4 = dict()
        news_data1 = dict()
        news_data2 = dict()
        list1 = list()
        list2 = list()
        temp_list1 = list()
        wiki_links = list()
        video_links = list()
        pdfs = list()
        images = list()
        scrape_data = ""
        no_of_links = 0
        no_of_scrape = 0
        wiki_scrape_temp = dict()
        scrape_data_dict = dict()
        scrape_data_dict_main = dict()
        colors = ["#111", "#f59042", "#555644", "#444"]
        print(result1)
        print(filters_list)

        for keyword in main_search_list:
            query = Keyword.objects.get_or_create()
            query.save()
            pipeline_result = crawling(keyword, filters_list)[2]

            for category, links in zip(filters_list, pipeline_result):
                cat = Category.objects.get_or_create(name=category)

                for link in links:
                    print(link[0])
                    if "wikipedia" in link[0]:
                        scrape_data, empty = wiki_scraping(link[0])
                        no_of_scrape += 1
                        wiki_links.append(link[0])
                        if not empty:
                            wiki_scrape_temp[str(link)] = scrape_data
                    elif link[0].endsWith("pdf"):
                        pdfs.append(link[0])
                    elif "youtube" in link[0]:
                        video_links.append(link[0])
                    else:
                        scrape_data = link[1]
                        images.append(extract_images(extract_images(scrape_data)))
                    scrape_data_dict[link[0]] = scrape_data
                    save_models.delay(
                        query.name,
                        cat.name,
                        link[0],
                        scrape_data,
                        reschedule_crawler,
                        userprofile.username,
                    )
            scrape_data_dict_main[keyword] = scrape_data_dict

        userprofile.scraped_data += no_of_scrape
        userprofile.save()

        if len(main_search_list) > 2:
            list1 = main_search_list[:2]
            list2 = main_search_list[:2]
        else:
            list1 = main_search_list
        
        for query in list1:
            result1[query] = crawling(query, filters_list)[0]
            temp_list1 = crawling(query, filters_list)[3]
            news_data1[query] = news(query)

        for query in list2:
            result3[query] = crawling(query, filters_list)[0]
            news_data2[query] = news(query)

        print(temp_list1)

        count_list1 = count_items(result1)
        count_list2 = count_items(result3)

        images_updated = list(filter(None, images))
        image_predict = category_predict(images_updated)

        random.shuffle(colors)

        context = {
            "home": True,
            "userprofile": userprofile,
            "notifications": notifications[:5],
            "unread_count": len(unread),
            "labels": filters_list,
            # 'result1': result2,
            # 'result2': result4,
            "list1": list1,
            "list2": list2,
            # 'count_list1': count_list1,
            # 'count_list2': count_list2,
            "temp_list1": temp_list1,
            "random_colors": colors,
            "news_data1": news_data1,
            "news_data2": news_data2,
            "wikis": wiki_scrape_temp,
            "main_search_list": main_search_list,
            "video_links": list(set(video_links))[:5],
            "pdfs": pdfs,
            "scrape_data_dict_main": scrape_data_dict_main,
            # 'images': images_updated,
            # 'image_predict': image_predict
        }

        return render(None, "crawler/process.html", context=context)


@login_required
def update(request):
    return True


@login_required
def update_notifications(request):
    return True


@login_required
def update_notifications_base(request):
    return True


@login_required
def read(request):
    return True
