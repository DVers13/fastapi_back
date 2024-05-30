FROM python:latest

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh