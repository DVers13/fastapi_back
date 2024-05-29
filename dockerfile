FROM python:3.11-slim

COPY . .

RUN chmod +x ./docker/app.sh

RUN pip install -r requirements.txt