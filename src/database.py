
"""
Script d'initialisation de la base de données SQLite pour Mairie-Cadeaux
"""
import sqlite3
from pathlib import Path
import json

DATABASE_PATH = Path(__file__).parent / "data" / "mairie.db"
#TABLES = ['homes', 'gifts', 'shipments', 'mails']
TABLES = ['gifts']

def init_database():
    """
    Crée toutes les tables nécessaires pour l'application.
    Si les tables existent déjà, elles ne sont pas recréées.
    """

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Connexion à la base de données
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Activer les clés étrangères (important pour les relations entre tables)
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Table Homes (Foyers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS homes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            firstname TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            postal_address TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Table Gifts (Cadeaux)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gifts (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            thumbnail TEXT,
            min_age INTEGER,
            max_age INTEGER,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Table Shipments (Envois)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id TEXT PRIMARY KEY,
            home_id TEXT NOT NULL,
            gift_id TEXT NOT NULL,
            ship_date TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (home_id) REFERENCES homes(id) ON DELETE CASCADE,
            FOREIGN KEY (gift_id) REFERENCES gifts(id) ON DELETE CASCADE
        )
    ''')
    
    # Table Mails (Emails)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mails (
            id TEXT PRIMARY KEY,
            shipment_id TEXT NOT NULL,
            mail_to TEXT NOT NULL,
            mail_from TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (shipment_id) REFERENCES shipments(id) ON DELETE CASCADE
        )
    ''')
    
    # Créer des index pour améliorer les performances des recherches
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_homes_email 
        ON homes(email)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_shipments_home_id 
        ON shipments(home_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_shipments_gift_id 
        ON shipments(gift_id)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_shipments_status 
        ON shipments(status)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_mails_shipment_id 
        ON mails(shipment_id)
    ''')
    
    # Sauvegarder les modifications
    conn.commit()
    
    # Afficher un résumé
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    conn.close()

def check_database_exist():
    db_path = Path(__file__).parent / "data" / "mairie.db"
    
    # Si le fichier n'existe pas, on doit créer et nourrir
    if not db_path.exists():
        return False
    return True

def drop_all_tables():
    """
    Supprime toutes les tables (utile pour réinitialiser complètement)
    ATTENTION: Cette fonction supprime toutes les données!
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    tables = ['mails', 'shipments', 'gifts', 'homes']
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
        print(f"Table {table} supprimée")
    
    conn.commit()
    conn.close()
    print("Toutes les tables ont été supprimées")

def fill_database():
    if not check_database_exist():
        init_database()

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    jsons_folder = Path(__file__).parent / "data"
    try:
        for table in TABLES:
            with open(jsons_folder / table + "json", 'r', encoding="utf-8") as file:
                content = json.load(file)
            
            for element in content:
                keys = element.keys()
                cursor.execute(
                    "INSERT INTO " + table + " (" + stringify_keys(keys) + ")" +
                    "VALUES (" + stringify_elements(element) + ")"
                )

                conn.commit()
        
        conn.close()
    except Exception as e:
        print(e)
        conn.close()

def stringify_keys(keys):
    string = ""
    for i in keys:
        string += str(i) + " "
    return string

def stringify_elements(dict):
    string = ""
    for i in dict.keys():
        string += str(dict[i]) + " "
    return string

def is_database_empty():
    """Vérifie si la base de données existe et est vide"""
    db_path = Path(__file__).parent / "data" / "mairie.db"
    
    # Si le fichier n'existe pas, la base est vide
    if not db_path.exists():
        return True
    
    # Si le fichier existe mais fait 0 bytes
    if db_path.stat().st_size == 0:
        return True
    
    return False

def is_data_empty():
    """
    Vérifie si la base de données a besoin d'être nourrie avec des données.
    """
    db_path = Path(__file__).parent / "data" / "mairie.db"
    
    # Si le fichier n'existe pas, on doit créer et nourrir
    if not db_path.exists():
        return True
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier les tables principales
        
        for table in TABLES:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            # Si au moins une table a des données, pas besoin de nourrir
            if count > 0:
                conn.close()
                return False
        
        # Toutes les tables sont vides
        conn.close()
        return True
        
    except sqlite3.OperationalError:
        # Les tables n'existent pas encore
        conn.close()
        return True

if __name__ == "__main__":
    jsons_folder = Path(__file__).parent.parent / "data"
    for table in TABLES:
        file = table + ".json"
        with open(jsons_folder / file, 'r', encoding="utf-8") as file:
            content = json.load(file)
        
        for element in content:
            keys = element.keys()
            print(stringify_elements(element))
            print(stringify_keys(keys))