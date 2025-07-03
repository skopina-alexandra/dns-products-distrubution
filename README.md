# dns-products-distrubution

## Запуск

1. Скопировать содержимое файла `.env.example` в файл `.env`.
2. Выполнить команды:
    - Windows

        ```
        docker-compose up --build
        ```
    - Linux / MacOS

        ```
        chmod +x entrypoint.sh

        docker-compose up --build
        ```

## Структура

- Создание и наполнение таблиц: `migrations/versions/`.
- Алгоритм распределения: `src/distribute`