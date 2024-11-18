#!/bin/sh

echo "Esperando que la base de datos esté disponible..."

while ! nc -z $(echo $DATABASE_URL | sed -E 's/.*:\/\/(.*):.*@([a-zA-Z0-9.-]+):.*/\2/') 5432; do
  sleep 1
done

echo "Base de datos disponible. Ejecutando migraciones..."

python -m alembic upgrade head

psql $DATABASE_URL -f /app/init_data.sql

exec uvicorn main:app --host 0.0.0.0 --port 8000
