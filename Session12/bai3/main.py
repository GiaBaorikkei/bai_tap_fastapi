from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ShipmentUpdate
from services import update_shipment_service

app = FastAPI()

# Cập nhật đơn hàng 
@app.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int, shipment_update: ShipmentUpdate, db: Session= Depends(get_db)):
    return update_shipment_service(shipment_id, shipment_update, db)

