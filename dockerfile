FROM python:3.11.9

RUN pip install--upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh