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
    path('scheduler/', include('scheduler.urls'), name='scheduler'),
    path('test/', views.test, name='test'),
    path("result/", view=views.process, name="process"),
    path("update/", view=views.update, name="update"),
    path("update-notifications/", view=views.update_notifications, name="update_notifications"),
    path("update-notifications-base/", view=views.update_notifications_base, name="update_notifications_base"),
]
