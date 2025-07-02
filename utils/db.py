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
