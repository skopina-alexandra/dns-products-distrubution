# from src.distribute import distribute
from src.distribute import distribute
from dotenv import load_dotenv
import logging

if __name__ == "__main__":

    load_dotenv() # загружаем переменные окружения
    logging.basicConfig(level=logging.INFO)

    distribute()
