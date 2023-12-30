from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from crawler.models import UserProfile, Notifications