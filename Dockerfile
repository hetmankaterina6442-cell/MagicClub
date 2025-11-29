FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# системні бібліотеки для Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libjpeg62-turbo-dev zlib1g-dev libwebp-dev libopenjp2-7-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# код додатку
COPY . .

# каталоги для статик/медіа
RUN mkdir -p /app/staticfiles /app/media

# без root
RUN useradd -m app && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["./entrypoint.sh"]
