#!/bin/bash
set -e

echo " [ms-convocatorias] Esperando MySQL en $DB_HOST:$DB_PORT..."
until php -r "
try {
    new PDO('mysql:host='.getenv('DB_HOST').';port='.getenv('DB_PORT').';dbname='.getenv('DB_DATABASE'), getenv('DB_USERNAME'), getenv('DB_PASSWORD'));
    echo 'ok';
} catch (Exception \$e) { exit(1); }
" 2>/dev/null | grep -q ok; do
    echo "  → MySQL no listo, reintentando en 3s..."
    sleep 3
done
echo "✅ MySQL disponible"

if [ -z "$APP_KEY" ]; then
    echo " Generando APP_KEY..."
    php artisan key:generate --force
fi

php artisan jwt:secret --force || true
php artisan config:clear
php artisan route:clear

echo "🔄 Ejecutando migraciones..."
php artisan migrate --force

echo "🚀 Iniciando ms-convocatorias en :8002"
exec php artisan serve --host=0.0.0.0 --port=8002
