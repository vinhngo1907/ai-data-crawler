from crawler import views
from django.urls import path, include

app_name = "crawler"

urlpatterns = [
    path("/dashborad", views.index, name="index"),
    path("crawler/", views.crawler_index, name="crawler_index"),
]
