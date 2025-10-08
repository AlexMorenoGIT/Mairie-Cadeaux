"""
Service contenant la logique métier pour les foyers
"""
from typing import List, Dict, Optional
import datetime
import uuid
from src.models.home import HomeModel


class HomesService:

    @staticmethod
    def get_all_homes() -> List[Dict]:
        """Récupère tous les foyers"""
        return HomeModel.get_all()

    @staticmethod
    def get_home_by_id(home_id: str) -> Optional[Dict]:
        """Récupère un foyer spécifique"""
        return HomeModel.get_by_id(home_id)

    @staticmethod
    def create_home(data: Dict) -> Dict:
        """
        Crée un nouveau foyer avec validation
        """
        # Validation
        required_fields = ['name', 'firstname', 'birth_date', 'email', 'postal_address']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Le champ '{field}' est obligatoire")

        # Vérifier si l'email existe déjà
        existing = HomeModel.get_by_email(data['email'])
        if existing:
            raise ValueError("Cet email est déjà utilisé")

        # Générer ID et date de création
        home_data = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'firstname': data['firstname'],
            'birth_date': data['birth_date'],
            'email': data['email'],
            'postal_address': data['postal_address'],
            'created_at': datetime.date.today().isoformat()
        }

        home_id = HomeModel.create(home_data)
        return HomeModel.get_by_id(home_id)

    @staticmethod
    def update_home(home_id: str, data: Dict) -> Optional[Dict]:
        """Met à jour un foyer"""
        # Vérifier que le foyer existe
        existing = HomeModel.get_by_id(home_id)
        if not existing:
            return None

        HomeModel.update(home_id, data)
        return HomeModel.get_by_id(home_id)

    @staticmethod
    def delete_home(home_id: str) -> bool:
        """Supprime un foyer"""
        existing = HomeModel.get_by_id(home_id)
        if not existing:
            return False

        return HomeModel.delete(home_id)

    @staticmethod
    def get_homes_eligible() -> List[Dict]:
        return HomeModel.get_eligible()