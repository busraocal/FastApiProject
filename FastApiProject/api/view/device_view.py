from ..model import SESSION_LOCAL, Device, Location, DeviceCreate
from fastapi import APIRouter
from ..controller import logger

session = SESSION_LOCAL()
router = APIRouter()


@router.get("/all_device_list")
async def device_list():
    entry = session.query(Device)
    data_list = object_to_dict(entry)
    if len(data_list) == 0:
        return []
    return data_list


@router.get("/device/{id}")
async def device(id: int):
    entry = session.query(Device).filter(Device.id == id)
    data_list = object_to_dict(entry)
    if len(data_list) == 0:
        return []
    return data_list


@router.post("/insert_device")
async def insert_device(device: DeviceCreate):
    device_model = Device(**device.dict())
    session.add(device_model)
    session.commit()
    logger.log_action(action="Device added.", data={"id": device_model.id, "name": device_model.name,
                                                    "created_date": device_model.created_date})
    return {"message": "Successfull"}


@router.delete("/delete_device/{id}")
async def delete_device(id: int):
    try:
        device_model_to_delete = session.query(Device).filter(Device.id == id).first()
        session.delete(device_model_to_delete)
        session.commit()
        device_info = device_model_to_delete.__dict__
        device_info.pop("_sa_instance_state")
        logger.log_action(action="Device deleted.", data=device_info)
        return {"message": "Deleted"}
    except Exception as ex:
        return {"message": ex}


def object_to_dict(entry):
    data_list = []
    for index in entry:
        data = index.__dict__
        data = {key: value for key, value in data.items() if not key.startswith('_')}
        data_list.append(data)

    if len(data_list) == 0:
        return []
    return data_list
