import os


def get_database_url():
    # Обработка переменных окружения с дефолтными значениями
    return (
        f"postgresql+psycopg2://"
        f"{os.environ.get('POSTGRES_DB_USER')}:"
        f"{os.environ.get('POSTGRES_DB_PASSWORD')}@"
        f"{os.environ.get('POSTGRES_DB_HOST')}:"
        f"{os.environ.get('POSTGRES_DB_PORT')}/"
        f"{os.environ.get('POSTGRES_DB_NAME')}"
    )


def get_database_connection_params():
    return {
        "dbname": os.environ.get("POSTGRES_DB_NAME"),
        "user": os.environ.get("POSTGRES_DB_USER"),
        "password": os.environ.get("POSTGRES_DB_PASSWORD"),
        "host": os.environ.get("POSTGRES_DB_HOST"),
        "port": os.environ.get("POSTGRES_DB_PORT"),
    }
