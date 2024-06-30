import os

import datetime
from datetime import timedelta

from celery import Celery
from celery.beat import crontab
from celery.utils.log import get_task_logger

import feedparser
from openai import OpenAI, OpenAIError

from news_aggregator.database.operations import get_last_pubdate_fromdb, create_article


client = OpenAI(api_key=os.getenv("API_KEY"))

app = Celery("tasks")
app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

logger = get_task_logger(__name__)


def fetch_rss_feed(url):
    return feedparser.parse(url).entries

@app.task(name="tasks.extract_news")
def extract_news(rss: str):
    """
    Get news list from rss
    rss: str link to rss feed
    """
    blog_feed = fetch_rss_feed(rss)
    return blog_feed

@app.task(name="tasks.extract_trends")
def extract_trends(rss: str) -> list:
    """
    Method to get last 7 days of trend news in Ukraine
    rss: str link to rss with trend news
    """
    feeds = []
    for i in range(7):
        date = (datetime.datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"{rss}?geo=UA&date={date}"
        feeds.extend(fetch_rss_feed(url))
    return feeds

@app.task(name="tasks.load_data")
def load_data(news: list[dict], trend_news=list):
    """
    Method to calculate sentiment score and in trend news and load them to database
    """
    datetime_format = "%a, %d %b %Y %H:%M:%S %z" # Format from tsnnews rss for datetime transforming
    last_pubdate = get_last_pubdate_fromdb() 
    if last_pubdate: # try to get last publication date from database and add to it 3 hours because column without timezone
        last_pubdate = last_pubdate.replace(hour=last_pubdate.hour+3, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800)))
    skip_sentiment_score = False # IF we have problems with openeai don't calculate sentiment score and set it to 0
    for feed in news:
        in_trend = False
        sentiment_score = 0
        published_date = datetime.datetime.strptime(feed["published"], datetime_format)
        if last_pubdate and (published_date <= last_pubdate): # if last publication date exists and given article is older than exists in database - skip
            continue
        if len(feed.description) > 500:
            logger.warn("Not article, probably a video, skipped")
            continue
        
        for trend in trend_news:
            if trend in clear_special_characters(feed["fulltext"]).lower(): # check if trend article is in feeds text
                in_trend = True
                break
        try:
            if not skip_sentiment_score:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                        "role": "system",
                        "content": "You will be provided with a feed and your task is to generate sentiment score for it. Output: floating point number. No comments before and after."
                        },
                        {
                        "role": "user",
                        "content": feed["fulltext"]
                        }
                    ],
                    temperature=0.7,
                    max_tokens=64,
                    top_p=1
                    )
                sentiment_score = float(response.choices.message.content)
        except OpenAIError as e:
            logger.warn("Something wrong with your openai account or key, check it to use sentiment score")
            skip_sentiment_score = True # If we have a problems with openai - skip sentiment score calculation for one task
        create_article(feed.description, feed.link, published_date, feed.title, sentiment_score, in_trend)

def clear_special_characters(string: str) -> str:
    return ''.join(letter for letter in string if letter.isalnum())

@app.task(name="tasks.etl")
def etl(news_rss: str, trend_news_rss: str):
    news = extract_news(news_rss)
    trend_news = extract_trends(trend_news_rss)
    trend_news_list = [clear_special_characters(feed["title"]).lower() for feed in trend_news]
    load_data(news=news, trend_news=trend_news_list)
