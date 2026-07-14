from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

tickets_db = [
    {"id": 1, "movie_name": "Doctor Strange 3", "room_code": "IMAX-01", "quantity": 2, "status": "confirmed"},
    {"id": 2, "movie_name": "Avatar 3", "room_code": "PREMIUM-02", "quantity": 1, "status": "confirmed"}
]

class CreateTicket(BaseModel):
    movie_name: str = Field(min_length=1)
    room_code: str = Field(min_length=1)
    quantity: int = Field(ge=1, le=10)

@app.get("/tickets")
def get_tickets():
    if not tickets_db:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Danh sách vé đang trống"
        )
    return {
        "statusCode": 200,
        "message": "Lấy danh sách vé thành công",
        "data": tickets_db,
    }
    
@app.post("/tickets")
def create_tickets(new_ticket: CreateTicket):
    ticket_id = len(tickets_db) + 1
    ticket_data = new_ticket.model_dump()
    for t in tickets_db:
        if t["movie_name"] == ticket_data["movie_name"] and t["room_code"] == ticket_data["room_code"]:
            raise HTTPException (
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lỗi: Vé xem phim tại phòng chiếu này đã được đặt!"
            )
    ticket = {
        "id": ticket_id,
        "movie_name": new_ticket.movie_name,
        "room_code": new_ticket.room_code,
        "quantity": new_ticket.quantity,
        "status": "confirmed"
    }
    tickets_db.append(ticket)
    return {
        "statusCode": 201,
        "message": "Đặt vé thành công",
        "data": ticket
    }
    
@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    for i in tickets_db:
        if i["id"] == ticket_id:
            tickets_db.remove(i)
            return {
                "statusCode": 200,
                "message": "Hủy vé thành công!",
            }
    raise HTTPException (
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Lỗi: Không tìm thấy mã vé yêu cầu!"
    )
    