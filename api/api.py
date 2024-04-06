from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import inspect
import settings as settings
import extensions
import managers


exts = extensions.get_extensions_initalized()
mgs = managers.get_managers_initalized()

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

def generate_routes(prefix, ext_name, module):
    for name, method in inspect.getmembers(module, inspect.ismethod):
        if name == "__init__": continue
        if name == "include": continue
        if not hasattr(method, 'included'): continue
        path = f"/{prefix}/{ext_name}/{name}/"

        tag = f"{prefix} - {ext_name}"
        if name == "get_data":
            path = f"/data/{prefix}/{ext_name}" 
            tag = "data"
        app.add_api_route(path, method, tags=[tag], methods=[method.request_type])

for name, ext in exts.items():
    generate_routes("extensions", name, ext)

for name, mg in mgs.items():
    generate_routes("managers", name, mg)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# uvicorn api:app --reload