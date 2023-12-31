from scheduler import views
from django.urls import path, include

app_name = 'scheduler'

urlpatterns = [
    path('', view=views.index, name='index'),
    path('search-link/', views.search, name='search'),
    path('scheduler-one/', views.scheduler_one, name='scheduler_one')
]