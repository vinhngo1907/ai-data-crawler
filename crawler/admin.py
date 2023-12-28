from django.contrib import admin
from .models import UserProfile, KeyWord, Category, Link, CrawledLinks, SocialMedia

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'crawled_links', 'scraped_data')
    search_fields = ['user']