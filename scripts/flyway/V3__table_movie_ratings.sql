create table movie_ratings (
    id      SERIAL     PRIMARY KEY     NOT NULL,
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating FLOAT,
    rating_timestamp BIGINT
)
