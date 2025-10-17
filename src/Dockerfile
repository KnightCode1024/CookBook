FROM python:3.14-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /app/www/src
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

