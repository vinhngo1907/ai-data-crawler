from celery import shared_task
from utils.crawler_spider import scraper
from utils.score import Score
from scheduler.models import ScrapedLink, RescrapedLink


@shared_task
def rescrape_one(old_link, new_data):
    check = Score()
    old_data = ScrapedLink.objects.get(link=old_link)
    score = check.total_score(old_data.scrape_data, new_data)
    done = False
    if score > 0:
        rescrape = RescrapedLink(
            link=old_data, scrape_data=new_data, score=score, done=True
        )
        rescrape.save()
        done = True

    return done
