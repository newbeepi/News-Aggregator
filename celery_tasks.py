from celery.beat import crontab
from news_aggregator.tasks import app

app.conf.beat_schedule = {
    # Executes every minute
    'executes etl process every minute': {
        'task': 'tasks.etl',
        'schedule': crontab(),
        'args': ("https://tsn.ua/rss/full.rss", "https://trends.google.com/trends/trendingsearches/daily/rss")
    },
}

if __name__ == "__main__":
    app.start()
