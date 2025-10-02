"""
API Flask pour Mairie-Cadeaux
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)

# Activer CORS pour autoriser les requêtes depuis React (localhost:5173)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Chemin vers le fichier homes.json
DATA_FILE_PATH = Path(__file__).parent / "data"

@app.route('/api/homes', methods=['GET'])
def load_homes():
    """Charge les foyers depuis le fichier JSON"""
    file = DATA_FILE_PATH / "homes.json"
    try:
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Erreur lors du chargement de homes.json: {e}")
        return []

# Base de données simulée pour les cadeaux (à garder si besoin)
gifts_db = [
    {"id": 1, "name": "Vélo électrique", "price": 800, "category": "Sport"},
    {"id": 2, "name": "Tablette", "price": 350, "category": "Électronique"},
    {"id": 3, "name": "Coffret bien-être", "price": 120, "category": "Détente"},
]

@app.route('/')
def index():
    """Page d'accueil de l'API"""
    return jsonify({
        "message": "Bienvenue sur l'API Mairie-Cadeaux",
        "version": "1.0.0",
        "endpoints": {
            "gifts": "/api/gifts",
            "gift_by_id": "/api/gifts/<id>",
        }
    })

@app.route('/api/gifts', methods=['GET'])
def get_gifts():
    """Récupère tous les cadeaux"""
    return jsonify(gifts_db)

@app.route('/api/gifts/<int:gift_id>', methods=['GET'])
def get_gift(gift_id):
    """Récupère un cadeau spécifique"""
    gift = next((g for g in gifts_db if g["id"] == gift_id), None)
    if gift:
        return jsonify(gift)
    return jsonify({"error": "Cadeau non trouvé"}), 404

@app.route('/api/gifts', methods=['POST'])
def create_gift():
    """Crée un nouveau cadeau"""
    data = request.get_json()
    
    new_gift = {
        "id": len(gifts_db) + 1,
        "name": data.get("name"),
        "price": data.get("price"),
        "category": data.get("category", "Autre")
    }
    
    gifts_db.append(new_gift)
    return jsonify(new_gift), 201

@app.route('/api/gifts/<int:gift_id>', methods=['DELETE'])
def delete_gift(gift_id):
    """Supprime un cadeau"""
    global gifts_db
    gifts_db = [g for g in gifts_db if g["id"] != gift_id]
    return jsonify({"message": "Cadeau supprimé"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)