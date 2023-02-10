from fastapi import APIRouter
from db import bin_status, contact

router = APIRouter(
    prefix="/bin",
    tags=["bin"]
)

TRASH_CAN_VOLUME = 501519.3  # cm^3
TRASH_FILL_VOLUME = 2700.0  # cm^3


@router.put("/{bin_id}/add/{trash_count}")
def add_amount(bin_id: int, trash_count: int):
    add = (TRASH_FILL_VOLUME * trash_count / TRASH_CAN_VOLUME) * 100
    total_in_bin = round(bin_status.find_one({"bin_id": bin_id})["status"] + add, 4)
    bin_status.update_one({"bin_id": bin_id}, {"$set": {"status": total_in_bin}})
    return {"status": total_in_bin}


@router.put("/{bin_id}/reset")
def add_reset(bin_id: int):
    amount = bin_status.find_one({"bin_id": bin_id})["reset"] + 1
    bin_status.update_one({"bin_id": bin_id}, {"$set": {"reset": amount, "status": 0}})
    return {"message": "success"}