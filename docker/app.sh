#!/bin/bash

alembic upgrade head

cd src

# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

uvicorn main:app --host 149.154.70.230 --port 80