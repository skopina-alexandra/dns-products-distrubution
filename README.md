# Тестовое задание DNS


## Структура

- Создание и наполнение таблиц: `migrations/versions/`.
- Алгоритм распределения: `src/distribute`

## Запуск

1. Скопировать содержимое файла `.env.example` в файл `.env`.

2. Запуск через Docker:
    - Windows

        ```
        docker-compose up --build
        ```
    - Linux / MacOS

        ```
        chmod +x entrypoint.sh

        docker-compose up --build
        ```
3. Запуск через `venv`:

    1. Создайте виртуальное окружение:
    
         ```
         python -m venv venv
         ```
    2. Активируйте виртуальное окружение:

        - Windows:

            ```
            .\venv\Scripts\activate
            ```
        - Linux / MacOS:

            ```
            sudo chmod +x /venv/bin/activate

            /venv/bin/activate
            ```
    3. Установите `poetry`

        ```
        pip install poetry
        ```
    4. Установите зависимости проекта:

        ```
        poetry install --no-root
        ```
    5. Запустите приложение:

        ```
        python main.py
        ```


## Планы на будущее:

- Добавить тесты
- Разделить бизнес-логику и обращения к БД
- Оптимизировать миграции 
