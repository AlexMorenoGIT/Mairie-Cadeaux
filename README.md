# Mairie-Cadeaux

Application de gestion des foyers et cadeaux municipaux.

## Prérequis

### Installation de UV

#### Windows
**Option 1 : PowerShell**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Option 2 : winget**
```powershell
winget install --id=astral-sh.uv -e
```

#### macOS
**Option 1 : Homebrew**
```bash
brew install uv
```

**Option 2 : curl**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Vérification de l'installation
```bash
uv --version
```

## Installation du projet

### 1. Cloner le dépôt
```bash
git clone <url>
cd Mairie-Cadeaux
```

### 2. Synchroniser les dépendances
```bash
uv sync
```

### 3. Installer le projet en mode éditable
```bash
uv pip install -e .
```

## Utilisation

### Lancer l'application complète (Backend Flask + Frontend React)
```bash
uv run app
```

L'application sera accessible sur :
- Frontend : http://localhost:5173
- Backend API : http://localhost:5000

### Lancer uniquement le backend
```bash
uv run backend
```

Le backend sera accessible sur http://localhost:5000

## Pour reinitialiser la base de donnée : 
- Supprimez simplement le fichier mairie.db
- Ce fichier sera automatiquement recréé au lancement de l'app si l'app detecte qu'il n'est plus present / vide.
- Le fichier mairie.db est créé à partir des JSONs présents dans le dossier /data. Si vous souhaitez modifier les données de maniere un peu plus profondes pour des tests, modifier directement les jsons et supprimez le fichier mairie.db

## Structure du projet
```
Directory structure:
└── alexmorenogit-mairie-cadeaux/
    ├── README.md
    ├── pyproject.toml
    ├── data/
    │   ├── gifts.json
    │   ├── homes.json
    │   └── shipments.json
    ├── frontend/
    │   ├── README.md
    │   ├── eslint.config.js
    │   ├── index.html
    │   ├── package.json
    │   ├── vite.config.js
    │   └── src/
    │       ├── App.css
    │       ├── App.jsx
    │       ├── index.css
    │       ├── main.jsx
    │       ├── component/
    │       │   └── table.jsx
    │       └── pages/
    │           ├── HomeAddPage.jsx
    │           ├── HomeEditPage.jsx
    │           ├── HomeListPage.jsx
    │           ├── HomePage.jsx
    │           └── ShipmentsList.jsx
    └── src/
        ├── __init__.py
        ├── app.py
        ├── config.py
        ├── database.py
        ├── main.py
        ├── utils.py
        ├── models/
        │   ├── __init__.py
        │   ├── gifts.py
        │   ├── home.py
        │   └── shipments.py
        ├── routes/
        │   ├── __init__.py
        │   ├── gifts_routes.py
        │   ├── homes_routes.py
        │   └── shipments_routes.py
        └── services/
            ├── __init__.py
            ├── gift_service.py
            ├── homes_service.py
            └── shipments_service.py

```
## Technologies utilisées
- **Backend** : Flask, Flask-CORS
- **Frontend** : React, Vite, Tailwind CSS
- **Gestionnaire de paquets** : UV
