# Generated by Django 3.0.8 on 2023-12-30 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='/static/dummyuser.jpg', null=True, upload_to='profile_images')),
                ('crawled_links', models.IntegerField(default=0)),
                ('scraped_data', models.IntegerField(default=0)),
                ('concurrency', models.IntegerField(default=1)),
                ('recent_link', models.IntegerField(default=5)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('screen_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('tweet_url', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('hashtags', models.CharField(max_length=100)),
                ('likes', models.CharField(max_length=30)),
                ('retweets', models.CharField(max_length=30)),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.Keyword')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('read', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(max_length=250)),
                ('scrape_data', models.TextField(blank=True, max_length=3000)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.Category')),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.Keyword')),
            ],
        ),
        migrations.CreateModel(
            name='CrawledLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reschedule', models.IntegerField(default=3)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.Link')),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawler.UserProfile')),
            ],
        ),
    ]
