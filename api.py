from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import inspect

import settings

# Extensions
from extensions.weatherExtension import WeatherExtension
from extensions.spotifyExtension import SpotifyExtension


weatherExt = WeatherExtension()
spotifyExt = SpotifyExtension()


app = FastAPI()

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_settings()["allowed_origins"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return 200

@app.get("/{name}")
def get_data(name: str):
    try:
        if name == "weather":
            return weatherExt.get_data()
        elif name == "spotify":
            return spotifyExt.get_data()
    except:
            return 500
    return 404

def generate_routes(ext_name, module):
     for name, method in inspect.getmembers(module, inspect.ismethod):
            if name == "__init__": continue
            if name == "include": continue
            if not hasattr(method, 'included'): continue
            path = f"/{ext_name}/{name}/"

            tag = ext_name
            if name == "get_data":
                 path = f"/data/{ext_name}" 
                 tag = "data"
            app.add_api_route(path, method, tags=[tag], methods=[method.request_type])



generate_routes("weather", weatherExt)
generate_routes("spotify", spotifyExt)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn api:app --reload