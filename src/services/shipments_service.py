import uuid
import datetime
from typing import List, Dict, Optional

from src.models.shipments import ShipmentModel
from src.services.gift_service import GiftsService
from src.models.home import HomeModel

class ShipmentsService:
    @staticmethod
    def get_all_shipments() -> List[Dict]:
        return  ShipmentModel.get_all()

    @staticmethod
    def create_shipment(home_id: str) -> Optional[Dict]:
        linked_home = HomeModel.get_by_id(home_id)
        if not linked_home:
            return None  # ou raise ValueError("Foyer introuvable")

        age_home = linked_home.get('birth_date')
        if not age_home:
            return None  # ou raise ValueError("Date de naissance manquante")

        birth_date = datetime.date.fromisoformat(age_home)
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        gift = GiftsService.get_gift_by_age(age)
        if not gift:
            return None  # ou raise ValueError("Aucun cadeau pour cet âge")

        shipment_data = {
            'id': str(uuid.uuid4()),
            'home_id': home_id,
            'gift_id': gift['id'],
            'status': "EXPEDIE",
            'created_at': datetime.date.today().isoformat(),
        }
        shipment_id = ShipmentModel.create(shipment_data)
        return ShipmentModel.get_by_id(shipment_id)

    @staticmethod
    def get_shipment(shipment_id: str) -> Optional[Dict]:
        return ShipmentModel.get_by_id(shipment_id)

    @staticmethod
    def get_shipment_by_home(home_id: str) -> Optional[Dict]:
        return ShipmentModel.get_by_home_id(home_id)

    @staticmethod
    def get_shipment_by_date(date: str) -> List[Dict]:
        return ShipmentModel.get_shipment_by_date(date)

    @staticmethod
    def delete_shipment_by_home_id(home_id: str) -> bool:
        return ShipmentModel.delete_by_home_id(home_id)
