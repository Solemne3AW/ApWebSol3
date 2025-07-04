# Etapa de construcción

FROM python:3.9-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Etapa de ejecución

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app/requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/root/.local/bin:$PATH
ENV DJANGO_ENV=production
ENV DATABASE_URL=postgres://user:pass@db:5432/medical_db

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]