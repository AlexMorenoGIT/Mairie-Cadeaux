"""
Configuration globale de l'application
"""
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "mairie.db"


# Configuration Flask
class Config:
    DEBUG = True

    # CORS
    CORS_ORIGINS = ["http://localhost:5173"]

    # Database
    DATABASE = DATABASE_PATH