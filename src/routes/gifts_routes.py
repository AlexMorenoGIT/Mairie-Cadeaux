from flask import Blueprint, jsonify

from src.services.gift_service import GiftsService

gifts_bp = Blueprint('gifts', __name__, url_prefix='/api/gifts')

@gifts_bp.route('', methods=['GET'])
def get_gifts():
    try:
        gifts = GiftsService.get_all_gifts()
        return jsonify(gifts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gifts_bp.route('/age/<age>', methods=['GET'])
def get_gift_age(age):
    try:
        gifts = GiftsService.get_gift_by_age(age)
        return jsonify(gifts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
