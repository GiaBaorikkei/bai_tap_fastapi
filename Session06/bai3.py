from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

rooms = [
    {"id": 1, "code": "R101", "name": "Room 101", "capacity": 30, "status": "AVAILABLE"},
    {"id": 2, "code": "R102", "name": "Room 102", "capacity": 20, "status": "AVAILABLE"},
    {"id": 3, "code": "R103", "name": "Room 103", "capacity": 40, "status": "MAINTENANCE"}
]

room_bookings = [
    {
        "id": 1,
        "room_id": 1,
        "class_name": "Python Basic",
        "student_count": 25,
        "date": "2026-07-01",
        "slot": "MORNING"
    }
]

class RoomRequest(BaseModel):
    id: int
    code: str
    name: str
    capacity: int = Field(gt=0)
    status: str


class BookingRequest(BaseModel):
    room_id: int
    class_name: str
    student_count: int = Field(gt=0)
    date: str
    slot: str
    
@app.post("/rooms")
def create_room(request: RoomRequest):

    if request.status not in ["AVAILABLE", "IN_USE", "MAINTENANCE"]:
        return {"message": "Invalid status"}

    if request.name.strip() == "":
        return {"message": "Name cannot be empty"}

    for room in rooms:
        if room["code"] == request.code:
            return {"message": "Code already exists"}

    rooms.append(request.model_dump())

    return {
        "message": "Create successfully",
        "data": request
    }
    
@app.get("/rooms/{room_id}")
def get_room(room_id: int):

    for room in rooms:
        if room["id"] == room_id:
            return room

    return {
        "message": "Room not found"
    }
    
@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    for room in rooms:
        if room["id"] == room_id:
            rooms.remove(room)
            return {
                "message": "Delete successfully"
            }

    return {
        "message": "Room not found"
    }
    
@app.post("/room-bookings")
def create_booking(request: BookingRequest):

    if request.slot not in ["MORNING", "AFTERNOON", "EVENING"]:
        return {"message": "Invalid slot"}

    room = None

    for r in rooms:
        if r["id"] == request.room_id:
            room = r
            break

    if room is None:
        return {"message": "Room not found"}

    if room["status"] != "AVAILABLE":
        return {"message": "Room is not available"}

    if request.student_count > room["capacity"]:
        return {"message": "Room capacity exceeded"}

    for booking in room_bookings:
        if booking["room_id"] == request.room_id and booking["date"] == request.date and booking["slot"] == request.slot:
            return {"message": "Room already booked"}

    new_booking = {
        "id": len(room_bookings) + 1,
        **request.model_dump()
    }

    room_bookings.append(new_booking)

    return {
        "message": "Booking successfully",
        "data": new_booking
    }
    
