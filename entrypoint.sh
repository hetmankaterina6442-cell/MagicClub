#!/bin/sh
set -e

# якщо бд змонтована файлом і його ще немає — створимо
[ -f /app/db.sqlite3 ] || touch /app/db.sqlite3

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn winxsite.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers ${GUNICORN_WORKERS:-3} \
  --timeout 60
