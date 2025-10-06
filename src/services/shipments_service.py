import uuid
import datetime
from typing import List, Dict, Optional

from src.models.shipments import ShipmentModel
from src.services.gift_service import GiftsService
from src.services.homes_service import HomesService


class ShipmentsService:
    @staticmethod
    def get_all_shipments() -> List[Dict]:
        return  ShipmentModel.get_all()

    @staticmethod
    def create_shipment(home_id: str) -> Optional[Dict]:
        linked_home = HomesService.get_home_by_id(home_id)
        age_home = linked_home['birth_date']
        birth_date = datetime.date.fromisoformat(age_home)
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        giftid = GiftsService.get_gift_by_age(age)

        shipment_data = {
            'id': str(uuid.uuid4()),
            'home_id': home_id,
            'gift_id': giftid['id'],
            'status': "EXPEDIE",
            'created_at': datetime.date.today().isoformat(),
        }
        shipment_id = ShipmentModel.create(shipment_data)
        return ShipmentModel.get_by_id(shipment_id)

    @staticmethod
    def get_shipment(shipment_id: str) -> Optional[Dict]:
        return ShipmentModel.get_by_id(shipment_id)

    @staticmethod
    def get_shipment_by_date(date: str) -> List[Dict]:
        return ShipmentModel.get_shipment_by_date(date)
