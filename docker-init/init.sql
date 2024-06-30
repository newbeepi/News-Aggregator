CREATE TABLE IF NOT EXISTS news (
    new_id INT GENERATED ALWAYS AS IDENTITY, -- Article ID
    headline VARCHAR(500),  -- Article Headline
    link VARCHAR(500), -- Link to article
    pub_date TIMESTAMP, -- Article publication date
    title VARCHAR(500), -- Title
    sentiment_score NUMERIC(10, 9), -- Sentimen't score from -1.0 to 1.0
    in_trend BOOLEAN -- Is this article in trend?
);