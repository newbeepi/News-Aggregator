from . import conn

from datetime import datetime

def get_last_pubdate_fromdb() -> datetime:
    """
    Get the newest feed we have from database
    """
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT MAX(pub_date)
            FROM news;
        """)
        return cursor.fetchone()[0]

def create_article(headline: str, 
                   link: str, 
                   pub_date: datetime, 
                   title: str, 
                   sentiment_score: float, 
                   in_trend: bool) -> None:
    """
    Save feed into news table
    """
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO news(headline, link, pub_date, title, sentiment_score, in_trend)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (headline, link, pub_date, title, sentiment_score, in_trend))
        conn.commit()

def get_relevant_news():
    """
    Get list of relevant feeds ordered by sentiment score
    """
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT * 
            FROM NEWS
            WHERE in_trend IS TRUE
            ORDER BY sentiment_score DESC;
        """)
        return cursor.fetchall()
