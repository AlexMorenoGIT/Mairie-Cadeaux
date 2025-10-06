"""
Fonctions utilitaires réutilisables
"""
import sqlite3
from typing import List, Dict, Any
from src.config import Config


def get_db_connection():
    """Crée une connexion à la base de données"""
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row  # Pour avoir des résultats sous forme de dict
    return conn


def dict_factory(cursor, row):
    """Transforme une ligne SQL en dictionnaire"""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Exécute une requête SELECT et retourne les résultats"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    columns = [description[0] for description in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()
    return results


def execute_update(query: str, params: tuple = ()) -> int:
    """Exécute une requête INSERT/UPDATE/DELETE"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id