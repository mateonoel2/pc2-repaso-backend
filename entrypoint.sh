#!/bin/bash
# Espera a que la base de datos esté disponible antes de ejecutar las migraciones

echo "Esperando que la base de datos esté disponible..."

while ! nc -z $(echo $DATABASE_URL | sed -E 's/.*:\/\/(.*):.*@([a-zA-Z0-9.-]+):.*/\2/') 5432; do
  sleep 1
done

echo "Base de datos disponible. Ejecutando migraciones..."

# Ejecuta las migraciones y llena la tabla con datos de animes
python -m alembic upgrade head

# Ejecuta el script de inicialización SQL para poblar la tabla de animes
psql $DATABASE_URL -f /app/init_data.sql

# Inicia la aplicación
exec uvicorn main:app --host 0.0.0.0 --port 8000
