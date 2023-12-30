from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications, Category
# from scheudler.models import ScrapedLink

from django.contrib import messages
# from utils.

@login_required
def index(request):
    """
    """
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    category = Category.objects.all()
    notifications = Notifications.objects.filter(user=userprofile).order_by('-pub_date')
    unread = notifications.filter(read=False)