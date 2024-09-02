FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "bot.py"]

# # Stage 1: установка зависимостей
# FROM python:3.11-slim AS builder

# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# WORKDIR /app

# RUN apt-get update \
#     && apt-get -y install libpq-dev gcc

# COPY requirements.txt .

# RUN python -m pip install --upgrade pip \
#     && pip install -r requirements.txt --no-cache-dir

# # Stage 2: финальный образ
# FROM python:3.11-slim

# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# WORKDIR /app

# COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
# COPY --from=builder /app .

# CMD ["python", "bot.py"]
