from fastapi import FastAPI
from api.model import *
from api.view import device_view, location_view

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    Device.metadata.create_all(bind=ENGINE)
    Location.metadata.create_all(bind=ENGINE)
    Log.metadata.create_all(bind=ENGINE)

    app.include_router(device_view.router)
    app.include_router(location_view.router)
