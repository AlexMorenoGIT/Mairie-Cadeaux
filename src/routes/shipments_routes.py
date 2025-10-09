"""
Blueprint Flask pour les routes /api/shipments
"""
from flask import Blueprint, jsonify, request

from src.services.shipments_service import ShipmentsService

# Créer le Blueprint
shipments_bp = Blueprint('shipments', __name__, url_prefix='/api/shipments')

@shipments_bp.route('', methods=['GET'])
def get_shipments():
    """GET /api/shipments - Liste tous les envoies"""
    try:
        shipments = ShipmentsService.get_all_shipments()
        return jsonify(shipments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shipments_bp.route('/<home_id>', methods=['POST'])
def create_shipment(home_id):
    """POST /api/shipments/<home_id> - Creates new shipment"""
    try:
        print(home_id)
        home_id = str(home_id)
        shipment = ShipmentsService.create_shipment(home_id)
        if shipment:
            return jsonify(shipment), 201
        else:
            return jsonify({"error": str(shipment)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shipments_bp.route('/<shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    """GET /api/shipments/<home_id> - Gets shipment"""
    try:
        shipment = ShipmentsService.get_shipment(shipment_id)
        if shipment:
            return jsonify(shipment), 200
        else:
            return jsonify({"error": str(shipment)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shipments_bp.route('/date/<date>', methods=['GET'])
def get_shipment_date(date):
    """GET /api/shipments/date/<date> - Gets shipment by date"""
    try:
        shipment = ShipmentsService.get_shipment_by_date(date)
        if shipment:
            return jsonify(shipment), 200
        else:
            return jsonify({"error": str(shipment)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500