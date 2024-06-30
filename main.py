from fastapi import FastAPI

from news_aggregator.database.operations import get_relevant_news as get_relevant_news_from_db

api = FastAPI()

def list_to_dict(input_list: list) -> dict:
    """
    Converts database result list into dict
    """
    resulted_dict = {
        "id": input_list[0],
        "headline": input_list[1],
        "link": input_list[2],
        "pub_date": input_list[3],
        "title": input_list[4], 
        "sentiment_score": input_list[5], 
        "in_trend": input_list[6]
    }
    return resulted_dict

@api.get("/get_relevant_news")
def get_relevant_news():
    """
    GET endpoint for getting list of relevant news from database
    """
    news = get_relevant_news_from_db()
    news_with_keys = [list_to_dict(new) for new in news]
    return news_with_keys
