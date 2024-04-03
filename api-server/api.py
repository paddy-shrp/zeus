from fastapi import FastAPI

# Extensions
from extensions.pHueLightsExtension import PHueExtension

# Start
# uvicorn main:app --reload

app = FastAPI()


@app.get("/")
def read_root():
    return 200


@app.put("/sensors/{id}")
def create_device(id: int, data: str | None = None):
    return {"id": id, "state": data}


# Extension creates API Path?
