#!/bin/sh

#waiting for db server to be ready to accept connections

echo 'Waiting for postgres...'

while ! nc -z $POSTGRES_DB_HOST $POSTGRES_DB_PORT; do
    sleep 0.1
done

echo 'PostgreSQL started'

echo 'Running migrations...'
poetry run alembic downgrade -1
poetry run alembic upgrade head


exec "$@"