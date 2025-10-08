"""
Modèle pour la table homes
"""
import datetime
from typing import List, Dict, Optional
from src.utils import execute_query, execute_update


class HomeModel:

    @staticmethod
    def get_all() -> List[Dict]:
        """Récupère tous les foyers"""
        query = "SELECT * FROM homes ORDER BY created_at DESC"
        return execute_query(query)

    @staticmethod
    def get_by_id(home_id: str) -> Optional[Dict]:
        """Récupère un foyer par son ID"""
        query = "SELECT * FROM homes WHERE id = ?"
        results = execute_query(query, (home_id,))
        return results[0] if results else None

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict]:
        """Récupère un foyer par son email"""
        query = "SELECT * FROM homes WHERE email = ?"
        results = execute_query(query, (email,))
        return results[0] if results else None

    @staticmethod
    def create(data: Dict) -> str:
        """Crée un nouveau foyer"""
        query = """
            INSERT INTO homes (id, name, firstname, birth_date, email, postal_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data['id'], data['name'], data['firstname'],
            data['birth_date'], data['email'], data['postal_address'],
            data['created_at']
        )
        execute_update(query, params)
        return data['id']

    @staticmethod
    def update(home_id: str, data: Dict) -> bool:
        """Met à jour un foyer"""
        query = """
            UPDATE homes 
            SET name = ?, firstname = ?, birth_date = ?, 
                email = ?, postal_address = ?
            WHERE id = ?
        """
        params = (
            data['name'], data['firstname'], data['birth_date'],
            data['email'], data['postal_address'], home_id
        )
        execute_update(query, params)
        return True

    @staticmethod
    def delete(home_id: str) -> bool:
        """Supprime un foyer"""
        query = "DELETE FROM homes WHERE id = ?"
        execute_update(query, (home_id,))
        return True

    @staticmethod
    def get_eligible() -> List[Dict]:
        """Récupérer les personnes éligibles"""
        datenow = datetime.date.today()
        date_last_year = datenow.replace(year=datenow.year - 1).isoformat()
        query = "SELECT * FROM homes WHERE  DATE(created_at) = ?"
        results = execute_query(query, (date_last_year,))
        return results

