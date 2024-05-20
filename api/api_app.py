from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

import api_routes
from zeus_core.utils import settings, paths

logging.basicConfig(filename=paths.get_logs_path("api_app.log"), encoding="utf-8", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_main_settings()["allowed_origins"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return 200

@app.get("/routes/{base:path}")
def get_routes(base):
    return [route.path for route in app.routes if route.path.startswith("/" + base)]

server = []

def start_api_app():
    global server

    api_routes.generate_modules_routes(app)
    logging.info("API is now running")
    
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    # ssl_crt = credentials.get_path("api.crt")
    # ssl_key = credentials.get_path("api.key")
    # config = uvicorn.Config(app, host="127.0.0.1", port=8000, ssl_certfile=ssl_crt, ssl_keyfile=ssl_key)
    start_api_app()
    
    

# uvicorn api:app --reload