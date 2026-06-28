# tasks.py
from celery import Celery
from celery.schedules import crontab
import subprocess

app = Celery('scraper_tasks', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'scrape-groceries-daily': {
        'task': 'tasks.run_spider',
        'schedule': crontab(hour=0, minute=0),
    },
}

@app.task
def run_spider():
    subprocess.run(["scrapy", "crawl", "grocery"])