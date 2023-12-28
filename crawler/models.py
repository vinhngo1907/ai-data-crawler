from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random, math


class KeyWord(models.Model):
    """
    Keywords Table
    """

    name = models.CharField(max_length=100, blank=False, null=False)
    pub_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower().replace(" ", "_")
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Link(models.Model):
    keyword = models.ForeignKey(KeyWord, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    scrape_data = models.TextField(max_length=250, blank=False, null=False)
    pub_dat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            str(self.link)
            + "for keyword "
            + str(self.keyword)
            + " in catetory"
            + str(self.category)
        )


class SocialMedia(models.Model):
    keyword = models.ForeignKey(KeyWord, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    screen_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    tweet_url = models.CharField(max_length=500)
    text = models.TextField(max_length=500)
    hashtags = models.CharField(max_length=100)
    likes = models.CharField(max_lengt=30)
    retweets = models.CharField(max_lengt=30)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(
        null=True, upload_to="profile_images", default="/static/dummyuser.jpg"
    )
    crawled_links = models.IntegerField(default=0)
    scraped_data = models.IntegerField(default=0)
    concurrency = models.IntegerField(default=1)
    recent_link = models.IntegerField(default=5)

    def __str__(self):
        return self.user.username

    def time_spent_scraping(self):
        now = timezone.now()
        diff = now - self.user.date_joined
        minutes = diff.total_seconds() / 3600

        return round(minutes, 1)

    def percent(self):
        result = random.randint(-3, 10)
        return (True, result) if result >= 0 else (False, -1 * result)
