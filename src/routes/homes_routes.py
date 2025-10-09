"""
Blueprint Flask pour les routes /api/homes
"""
import datetime

from flask import Blueprint, jsonify, request

from src.services.gift_service import GiftsService
from src.services.homes_service import HomesService

# Créer le Blueprint
homes_bp = Blueprint('homes', __name__, url_prefix='/api/homes')

@homes_bp.route('', methods=['GET'])
def get_homes():
    """GET /api/homes - Liste tous les foyers"""
    try:
        homes = HomesService.get_all_homes()
        return jsonify(homes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@homes_bp.route('/eligible', methods=['GET'])
def eligible():
    """GET /api/homes/eligible - Liste tous les foyers éligibles aujourd'hui"""
    try:
        success = HomesService.get_homes_eligible()
        if success :
            try:
                for home in success:
                    created_at_str = home.get('birth_date')
                    created_at_date = datetime.date.fromisoformat(created_at_str)
                    today = datetime.date.today()
                    age = today.year - created_at_date.year - (
                        (today.month, today.day) < (created_at_date.month, created_at_date.day)
                    )
                    gift = GiftsService.get_gift_by_age(age)
                    home['gift'] = gift
                return jsonify(success), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"message": "Pas de foyer éligible"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@homes_bp.route('/<home_id>', methods=['GET'])
def get_home(home_id):
    """GET /api/homes/<id> - Récupère un foyer"""
    try:
        home = HomesService.get_home_by_id(home_id)
        if home:
            return jsonify(home), 200
        return jsonify({"error": "Foyer non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@homes_bp.route('', methods=['POST'])
def create_home():
    """POST /api/homes - Crée un foyer"""
    try:
        data = request.get_json()
        home = HomesService.create_home(data)
        return jsonify(home), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@homes_bp.route('/<home_id>', methods=['PUT'])
def update_home(home_id):
    """PUT /api/homes/<id> - Met à jour un foyer"""
    try:
        data = request.get_json()
        home = HomesService.update_home(home_id, data)
        if home:
            return jsonify(home), 200
        return jsonify({"error": "Foyer non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@homes_bp.route('/<home_id>', methods=['DELETE'])
def delete_home(home_id):
    """DELETE /api/homes/<id> - Supprime un foyer"""
    try:
        success = HomesService.delete_home(home_id)
        if success:
            return jsonify({"message": "Foyer supprimé"}), 200
        return jsonify({"error": "Foyer non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


