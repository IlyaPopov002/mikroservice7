FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_receipt

# Установка зависимостей проекта
COPY ./app_receipt/requirements.txt /app_receipt/
RUN pip install --no-cache-dir --upgrade -r /app_receipt/requirements.txt

# Перенос проекта в образ
COPY ./app_receipt/app /app_receipt/app
COPY .env /app_receipt

# Копирование файлов alembic
COPY ./app_receipt/migration /app_receipt/migration
COPY ./app_receipt/alembic.ini /app_receipt/alembic.ini

EXPOSE 81

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 81"]