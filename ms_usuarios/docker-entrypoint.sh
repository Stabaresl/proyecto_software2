#!/bin/bash
set -e

echo " [ms-usuarios] Esperando PostgreSQL en $DB_HOST:$DB_PORT..."
until python -c "
import psycopg2, os, sys
try:
    psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
except Exception as e:
    sys.exit(1)
" 2>/dev/null; do
    echo "  → PostgreSQL no listo, reintentando en 3s..."
    sleep 3
done
echo "✅ PostgreSQL disponible"

echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "🚀 Iniciando ms-usuarios en :8001"
exec python manage.py runserver 0.0.0.0:8001
