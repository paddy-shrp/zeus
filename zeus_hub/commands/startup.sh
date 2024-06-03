#!/bin/bash

cd /root/tapit-server/tap-it/
source .venv/bin/activate
cd api
gunicorn api_app:app --bind 127.0.0.1:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker