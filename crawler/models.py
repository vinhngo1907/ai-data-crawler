from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random, math


class Keyword(models.Model):
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
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
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
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    screen_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    tweet_url = models.CharField(max_length=500)
    text = models.TextField(max_length=500)
    hashtags = models.CharField(max_length=100)
    likes = models.CharField(max_length=30)
    retweets = models.CharField(max_length=30)


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

    def concurrency_percent(self):
        result = (self.concurrency / 10) * 100


class CrawledLinks(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    reschedule = models.IntegerField(default=3)
    pub_date = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):
        now = timezone.now()
        diff = now - self.pub_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + "seconds ago"
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + "minute ago"
            else:
                return str(minutes) + "minutes ago"
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + "hour ago"
            else:
                return str(hours) + "hours ago"
        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + "day ago"
            else:
                return str(days) + "days ago"
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)
            if months == 1:
                return str(months) + "month ago"
            else:
                return str(months) + "months ago"
        if diff.days >= 365:
            years = math.floor(diff.days / 365)
            if years == 1:
                return str(years) + "year ago"
            else:
                return str(years) + "years ago"

    def __str__(self):
        return "by - " + self.userprofile.user.username


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100, blank=False, null=False)
    read = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):
        now = timezone.now()

        diff = now - self.pub_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def __str__(self):
        return self.user.username + " has new notification!!! " + str(self.pub_date)
