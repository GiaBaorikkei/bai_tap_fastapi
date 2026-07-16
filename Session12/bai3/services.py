from fastapi import HTTPException
from models import ShipmentUpdate, ShipmentModel

def update_shipment_service(shipment_id: int, shipment_update: ShipmentUpdate, db):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id==shipment_id).first()
    if shipment is None:
        raise HTTPException (
            status_code=404,
            detail="Không tìm thấy đơn hàng để cập nhật"
        )
    shipment.receiver_name = shipment_update.receiver_name
    shipment.delivery_address = shipment_update.delivery_address
    db.commit()
    db.refresh(shipment)
    return {
        "message": "Cập nhật đơn hàng thành công",
        "data": shipment
    }
    
    