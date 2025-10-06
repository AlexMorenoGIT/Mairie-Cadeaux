
"""
Script d'initialisation de la base de données SQLite pour Mairie-Cadeaux
"""
import sqlite3
from pathlib import Path
import json
import traceback

DATABASE_PATH = Path(__file__).parent.parent / "data" / "mairie.db"
TABLES = ['homes', 'gifts', 'shipments', 'mails']


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
    
    conn.close()

def check_database_exist():
    
    # Si le fichier n'existe pas, on doit créer et nourrir
    if not DATABASE_PATH.exists():
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

    jsons_folder = Path(__file__).parent.parent / "data"
    try:
        for table in TABLES:
            file = table + ".json"
            with open(jsons_folder / file, 'r', encoding="utf-8") as file:
                content = json.load(file)
            
            for element in content:
                keys = element.keys()
                columns = ", ".join(element.keys())
                placeholders = ", ".join(["?"] * len(keys))
                values = tuple(element.values())
                cursor.execute(
                    f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                    values
                )
            print("Table [" + table + "] filled.")

            conn.commit()
        
        conn.close()
    except Exception as e:
        print(e)
        traceback.print_exc()
        conn.close()

def is_database_empty():
    
    # Si le fichier n'existe pas, la base est vide
    if not DATABASE_PATH.exists():
        return True
    
    # Si le fichier existe mais fait 0 bytes
    if DATABASE_PATH.stat().st_size == 0:
        return True
    
    return False

def is_data_empty():
    """
    Vérifie si la base de données a besoin d'être nourrie avec des données.
    """
    db_path = Path(__file__).parent.parent / "data" / "mairie.db"
    
    print(f"Chemin DB: {db_path}")
    print(f"Existe: {db_path.exists()}")
    
    if not db_path.exists():
        return True
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        for table in TABLES:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            if count > 0:
                conn.close()
                return False
        
        conn.close()
        return True
        
    except sqlite3.OperationalError as e:
        conn.close()

if __name__ == "__main__":
    print("Drop database . . .")
    drop_all_tables()
    print("Init database tables . . .")
    init_database()
    print("Fill database tables . . .")
    fill_database()