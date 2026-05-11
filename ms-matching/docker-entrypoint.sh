#!/bin/sh
set -e

echo " [ms-matching] Esperando MySQL en $DB_HOST:$DB_PORT..."
until node -e "
const mysql = require('mysql2');
const conn = mysql.createConnection({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});
conn.connect(err => {
  if (err) { conn.destroy(); process.exit(1); }
  conn.end();
  process.exit(0);
});
" 2>/dev/null; do
  echo "  → MySQL no listo, reintentando en 3s..."
  sleep 3
done

echo "✅ MySQL disponible"
echo "🚀 Iniciando ms-matching en :$PORT"
exec node src/server.js
