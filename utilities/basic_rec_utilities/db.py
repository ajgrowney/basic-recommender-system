

from email.policy import default


def get_conn_str(user, pwd, server, port = 5432, db_name = "postgres"):
    return f"postgresql+psycopg2://{user}:{pwd}@{server}:{port}/{db_name}"

def interaction_to_rating(interaction:str) -> float:
    """
    """
    MAPPING = {
        'HATE': 1.0,
        'DISLIKE': 2.0,
        'OK': 3.0,
        'LIKE': 4.0,
        'LOVE': 5.0
    }
    return MAPPING.get(interaction, 3.0)