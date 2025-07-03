import os
import logging
import time
import psycopg2


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


def create_db_connection():
    max_retries = 5
    retry_delay = 3  # секунды между попытками
    attempt = 0
    while attempt < max_retries:
        try:
            connection = psycopg2.connect(**get_database_connection_params())
            logging.info("Соединение с БД успешно установлено")
            return connection
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            attempt += 1
            logging.error(f"Ошибка подключения (попытка {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                logging.info(f"Повторная попытка через {retry_delay} сек...")
                time.sleep(retry_delay)
                retry_delay *= 1.5

    raise ConnectionError(f"Не удалось подключиться к БД после {max_retries} попыток")
