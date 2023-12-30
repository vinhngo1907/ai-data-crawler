from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Category, CrawledLinks
from scheduler.models import ScrapedLink
from django.db.models import Count
from django.contrib import messages
from utils.analytics import category_percent

@login_required
def index(request):
    """
    """
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    category = Category.objects.all()
    notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')
    unread = notifications.filter(read=False)
    user_crawled_links = CrawledLinks.objects.filter(userprofile=userprofile).order_by('-pub_date')
    context = dict()
    context['home'] = True
    context['category'] = category
    context['userprofile'] = userprofile
    context['notifications'] = notifications[5]
    context['unread_count'] = len(unread)
    context['user_crawled'] = user_crawled_links[:userprofile.recent_link]
    context['cat_percent'] = category_percent()