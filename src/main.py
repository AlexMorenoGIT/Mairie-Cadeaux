"""
Lanceur principal qui démarre Flask (backend) et Vue.js (frontend) simultanément
Usage: uv run python main.py
"""
import subprocess
import sys
import os
import time
from threading import Thread
from pathlib import Path

# Couleurs pour les logs
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def log(message, color=Colors.GREEN, function_name="System"):
    print(f"{color}{Colors.BOLD}[Mairie-Cadeaux][" + function_name + f"]{Colors.END} {message}")

def import_database():
    try:
        import src.database as database

        if not database.DATABASE_PATH.exists() or database.is_database_empty(): 
            log("Import de la base de donnée :", Colors.BLUE, "database")
            database.init_database()
            
            print("Base de données initialisée avec succès!")
            print(f"Emplacement: {database.DATABASE_PATH}")
        
        if database.is_data_empty():
            log("Remplissage des données :", Colors.BLUE, "database")
            database.fill_database()

    except Exception as e:
        log("Impossible d'importer la database : " + str(e), Colors.RED, "database")
        exit(0)

def run_backend():
    """Lance le serveur Flask sur le port 5000"""
    log("Démarrage du Backend Flask...", Colors.BLUE, "backend")
    try:
        from src.app import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except Exception as e:
        log(f"Erreur Backend: {e}", Colors.RED, "backend")
        sys.exit(1)

def run_frontend():
    """Lance le serveur de dev Vue.js (Vite)"""
    log("Démarrage du Frontend Vue.js...", Colors.BLUE, "frontend")
    
    frontend_path = Path(__file__).parent.parent / "frontend"
    print(frontend_path)
    if not frontend_path.exists():
        log("Le dossier 'frontend' n'existe pas!", Colors.RED, "frontend")
        log("Créez-le avec: npm create vue@latest frontend", Colors.YELLOW, "frontend")
        return
    
    # Vérifier si node_modules existe
    if not (frontend_path / "node_modules").exists():
        log("Installation des dépendances npm...", Colors.YELLOW, "frontend")
        subprocess.run(["npm", "install"], cwd=frontend_path, shell=True)
        return
    
    try:
        # Lance npm run dev
        process = subprocess.run(
            ["npm", "run", "dev"], 
            cwd=frontend_path, 
            shell=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        process.wait()
    except subprocess.CalledProcessError as e:
        log(f"Erreur Frontend: {e}", Colors.RED, "frontend")
        if sys.platform == 'win32':
            process.terminate()
        else:
            process.send_signal(signal.SIGINT)
    except KeyboardInterrupt:
        log("Arrêt du Frontend", Colors.YELLOW, "frontend")

def main():
    """Point d'entrée principal"""
    print("\n" + "="*60)
    log("Démarrage de l'application Mairie-Cadeaux", Colors.GREEN, "main")
    print("="*60 + "\n")
    
    # Initialisation de la database
    import_database()
    
    # Créer les threads pour lancer les deux serveurs
    backend_thread = Thread(target=run_backend, daemon=False)
    frontend_thread = Thread(target=run_frontend, daemon=False)
    
    # Démarrer le backend en premier
    backend_thread.start()
    time.sleep(2)  # Attendre que Flask démarre
    
    log("Backend lancé sur http://localhost:5000", Colors.GREEN, "main")
    
    # Puis démarrer le frontend
    frontend_thread.start()
    time.sleep(3)  # Attendre que Vite démarre
    
    log("Frontend lancé sur http://localhost:5173", Colors.GREEN, "main")
    
    print("\n" + "="*60)
    log("Application prête !", Colors.GREEN, "main")
    log("Frontend: http://localhost:5173", Colors.BLUE, "main")
    log("API Backend: http://localhost:5000/api", Colors.BLUE, "main")
    print("="*60)
    log("Appuyez sur Ctrl+C pour arrêter", Colors.YELLOW, "main")
    print()
    
    try:
        # Garder le programme en vie
        backend_thread.join()
        frontend_thread.join()
    except KeyboardInterrupt:
        print("\n")
        log("Arrêt de l'application...", Colors.YELLOW, "main")
        sys.exit(0)

if __name__ == "__main__":
    main()  