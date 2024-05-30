FROM python:3.10-slim

RUN pip install--upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh