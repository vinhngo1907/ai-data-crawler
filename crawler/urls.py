from crawler import views
from django.urls import path, include

app_name = "crawler"

urlpatterns = [
    path("dashboard/", views.index, name="index"),
    path("crawler/", views.crawler_index, name="crawler_index"),
    path("report/", views.report, name="report"),
    path("test/", views.test, name="test"),
    path("calendar/", views.calendar, name="calendar"),
    # path("social-scrape-data/", views.social, name="social"),
]
