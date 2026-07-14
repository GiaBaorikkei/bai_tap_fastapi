from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI()

desks = [
    {
        "id": 1,
        "desk_number": "DSK-A-01",
        "zone": "Zone A - Quiet Space",
        "price_per_day": 150000.0,
        "status": "AVAILABLE"
    },
    {
        "id": 2,
        "desk_number": "DSK-B-02",
        "zone": "Zone B - Creative",
        "price_per_day": 200000.0,
        "status": "AVAILABLE"
    },
    {
        "id": 3,
        "desk_number": "DSK-C-03",
        "zone": "Zone C - Panoramic",
        "price_per_day": 250000.0,
        "status": "MAINTENANCE"
    }
]

bookings = [
    {
        "id": 1,
        "desk_id": 1,
        "customer_name": "Nguyen Van A",
        "booking_date": "2026-07-01",
        "payment_status": "PAID"
    }
]

# ==========================
# MODELS
# ==========================

class DeskCreate(BaseModel):
    desk_number: str
    zone: str
    price_per_day: float = Field(gt=0)
    status: Literal["AVAILABLE", "UNAVAILABLE", "MAINTENANCE"]


class BookingCreate(BaseModel):
    desk_id: int
    customer_name: str
    booking_date: str
    payment_status: Literal["PENDING", "PAID", "CANCELLED"]


# ==========================
# DESK APIs
# ==========================

@app.post("/desks", status_code=status.HTTP_201_CREATED)
def create_desk(desk: DeskCreate):

    for item in desks:
        if item["desk_number"].lower() == desk.desk_number.lower():
            raise HTTPException(
                status_code=400,
                detail="Desk number already exists"
            )

    new_desk = desk.model_dump()

    if desks:
        new_desk["id"] = max(d["id"] for d in desks) + 1
    else:
        new_desk["id"] = 1

    desks.append(new_desk)

    return new_desk


@app.get("/desks")
def get_desks(
    zone_keyword: Optional[str] = None,
    max_price: Optional[float] = Query(None, gt=0),
    status: Optional[str] = None
):

    result = desks

    if zone_keyword:
        result = [
            d for d in result
            if zone_keyword.lower() in d["zone"].lower()
        ]

    if max_price is not None:
        result = [
            d for d in result
            if d["price_per_day"] <= max_price
        ]

    if status:
        result = [
            d for d in result
            if d["status"] == status
        ]

    return result


@app.get("/desks/{desk_id}")
def get_desk(desk_id: int):

    for desk in desks:
        if desk["id"] == desk_id:
            return desk

    raise HTTPException(
        status_code=404,
        detail="Desk not found"
    )


@app.put("/desks/{desk_id}")
def update_desk(desk_id: int, desk: DeskCreate):

    for index, item in enumerate(desks):

        if item["id"] == desk_id:

            for d in desks:
                if (
                    d["id"] != desk_id
                    and d["desk_number"].lower() == desk.desk_number.lower()
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Desk number already exists"
                    )

            update_data = desk.model_dump()
            update_data["id"] = desk_id

            desks[index] = update_data

            return update_data

    raise HTTPException(
        status_code=404,
        detail="Desk not found"
    )


@app.delete("/desks/{desk_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_desk(desk_id: int):

    for index, desk in enumerate(desks):

        if desk["id"] == desk_id:
            desks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404,
        detail="Desk not found"
    )


# ==========================
# BOOKING APIs
# ==========================

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):

    desk = None

    for d in desks:
        if d["id"] == booking.desk_id:
            desk = d
            break

    if desk is None:
        raise HTTPException(
            status_code=404,
            detail="Desk not found"
        )

    if desk["status"] != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Desk is not available"
        )

    for b in bookings:
        if (
            b["desk_id"] == booking.desk_id
            and b["booking_date"] == booking.booking_date
        ):
            raise HTTPException(
                status_code=400,
                detail="This desk has already been booked on this date"
            )

    new_booking = booking.model_dump()

    if bookings:
        new_booking["id"] = max(b["id"] for b in bookings) + 1
    else:
        new_booking["id"] = 1

    bookings.append(new_booking)

    return new_booking


@app.get("/bookings")
def get_bookings():
    return bookings