from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Category, Notifications
from scheduler.models import ScrapedLink, RescrapedLink
from django.shortcuts import render, HttpResponse
from scheduler.tasks import rescrape_one

@login_required
def index(request):
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    categories = Category.objects.all()
    notifications = Notifications.objects.filter(user=userprofile).order_by("-pub_date")
    unread = notifications.filter(read=False)
    scraped_links = ScrapedLink.objects.all()

    context = dict()
    context["userprofile"] = userprofile
    context["category"] = categories
    context["notifications"] = notifications[:5]
    context["unread"] = len(unread)
    context["scraped_links"] = scraped_links

    return render(request, "scheduler/index.html", context=context)



@login_required
def search(request):
    """
    :param request:
    :return:
    """
    empty = False
    if(request.method == "POST"):
        search = request.POST.get('data')
        scrape_link = ScrapedLink.objects.get(link=search)

        try:
            rescrape_link = RescrapedLink.objects.get(link=scrape_link)
        except:
            empty = True
            rescrape_link = "Not scrape link"

        context = {
            "scrape_link": scrape_link,
            "empty": empty,
            "rescrape_link": rescrape_link
        }
        
        return render(None, "scheduler/search.html", context=context)

@login_required
def scheduler_one(request):
    done, score = rescrape_one()
    return HttpResponse(f"done {done} and score is {score}")