from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import utils.settings as settings
import utils.credentials as credentials
import utils.paths as paths
import api_routes
import uvicorn
import logging

logging.basicConfig(filename=paths.get_logs_path("api.log"), encoding="utf-8", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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

api_routes.generate_modules_routes(app)

if __name__ == "__main__":
    # ssl_crt = credentials.get_path("api.crt")
    # ssl_key = credentials.get_path("api.key")
    # config = uvicorn.Config(app, host="127.0.0.1", port=8000, ssl_certfile=ssl_crt, ssl_keyfile=ssl_key)
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    server.run()
    

# uvicorn api:app --reload