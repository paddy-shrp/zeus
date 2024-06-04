#!/bin/bash

cd /Users/patr/Documents/GitHub/zeus

source .venv/bin/activate
cd api
gunicorn api_app:app --bind 127.0.0.1:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker &
cd ..
.venv/bin/python data/data_app.py &