from django.contrib import admin
from .models import (
    UserProfile,
    KeyWord,
    Notifications,
    Category,
    Link,
    CrawledLinks,
    SocialMedia,
)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "crawled_links", "scraped_data")
    search_fields = ["user"]


class NotificationsAdmin("user", "pub_date"):
    list_display = ("user", "pub_date")
    search_fields = ["user"]

    class Meta:
        verbose_name_plural = "Notifications"


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Notifications, NotificationsAdmin)
