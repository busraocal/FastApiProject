from ..model import SESSION_LOCAL, Location, LocationCreate
from fastapi import APIRouter
from sqlalchemy import func, and_
from queue import Queue
from ..controller import logger

q = Queue()
session = SESSION_LOCAL()
router = APIRouter()


@router.get("/device_location_history/{device_id}")
async def device_location_history(device_id: int):
    entry = session.query(Location).filter(Location.device_id == device_id)
    data_list = object_to_dict(entry)
    if len(data_list) == 0:
        return []
    return data_list


@router.get("/last_locations")
async def last_locations():
    subquery = session.query(Location.device_id, func.max(Location.created_date).label("max_created_date")).group_by(
        Location.device_id).subquery()
    last_locations_query = session.query(Location).join(subquery, and_(Location.device_id == subquery.c.device_id,
                                                                       Location.created_date == subquery.c.max_created_date)).all()
    data_list = object_to_dict(last_locations_query)
    if len(data_list) == 0:
        return []
    return data_list


@router.post("/insert_location")
async def insert_location(location: LocationCreate):
    q.put(location.dict())
    logger.log_action(action="Added to queue", data=location.dict())
    return {"message": "Request received and added to queue"}


@router.post("/process_queue")
async def process_queue():
    while not q.empty():
        location_data = q.get()
        location_model = Location(**location_data)
        session.add(location_model)
        session.commit()
        logger.log_action(action="Location added.",
                          data={"id": location_model.id, "device_id": location_model.device_id,
                                "location": location_model.location, "created_date": location_model.created_date})

    return {"message": "Queue processed"}


def object_to_dict(entry):
    data_list = []
    for index in entry:
        data = index.__dict__
        data = {key: value for key, value in data.items() if not key.startswith('_')}
        data_list.append(data)

    if len(data_list) == 0:
        return []
    return data_list
