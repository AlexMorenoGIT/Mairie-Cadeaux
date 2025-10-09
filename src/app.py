"""
Application Flask principale avec Blueprints
"""
from flask import Flask, jsonify
from flask_cors import CORS
from src.config import Config

# Importer tous les blueprints
from src.routes.homes_routes import homes_bp
from src.routes.shipments_routes import shipments_bp
from src.routes.gifts_routes import gifts_bp


def create_app():
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuration CORS
    CORS(app, resources={
        r"/api/*": {"origins": Config.CORS_ORIGINS}
    })

    # Enregistrer les blueprints
    app.register_blueprint(homes_bp)
    app.register_blueprint(shipments_bp)
    app.register_blueprint(gifts_bp)

    # Route d'accueil
    @app.route('/')
    def index():
        return jsonify({
            "message": "API Mairie-Cadeaux",
            "version": "2.0.0",
            "endpoints": {
                "homes": "/api/homes",
                "gifts": "/api/gifts",
                "shipments": "/api/shipments",
                "mails": "/api/mails"
            }
        })

    return app

# Pour le lancement direct
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)