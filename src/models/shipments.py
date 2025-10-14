import datetime
from typing import List, Dict, Optional

from src.utils import execute_query, execute_update


class ShipmentModel:
    @staticmethod
    def get_all() -> List[Dict]:
        query = "SELECT * FROM shipments ORDER BY created_at DESC"
        return execute_query(query)

    @staticmethod
    def get_by_id(shipment_id: str) -> Optional[Dict]:
        query = "SELECT * FROM shipments WHERE id = ?"
        result = execute_query(query, (shipment_id,))
        return result[0] if result else None

    @staticmethod
    def get_by_home_id(home_id: str) -> Optional[Dict]:
        query = "SELECT * FROM shipments WHERE home_id = ?"
        result = execute_query(query, (home_id,))
        return result[0] if result else None

    @staticmethod
    def create(data: Dict) -> str:
        query = """
            INSERT INTO shipments (id, home_id, gift_id, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (
            data['id'],
            data['home_id'],
            data['gift_id'],
            data['status'],
            data['created_at']
        )
        execute_update(query, params)
        return data['id']

    @staticmethod
    def get_shipment_by_date(date: str) -> List[Dict]:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La date doit être au format 'YYYY-MM-DD'")
        query = "SELECT * FROM shipments WHERE created_at = ?"
        result = execute_query(query, (date,))
        return result

    @staticmethod
    def delete_by_home_id(home_id: str) -> bool:
        """Supprime un shipment"""
        query = "DELETE FROM shipments WHERE home_id = ?"
        execute_update(query, (home_id,))
        return True