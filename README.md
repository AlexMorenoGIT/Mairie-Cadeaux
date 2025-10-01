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

## Structure du projet
```
Mairie-Cadeaux/
├── src/
│   ├── main.py          # Point d'entrée principal
│   ├── app.py           # API Flask
│   └── data/
│       └── homes.json   # Base de données des foyers
├── frontend/            # Application React
├── pyproject.toml       # Configuration du projet
└── README.md
```

## Technologies utilisées
- **Backend** : Flask, Flask-CORS
- **Frontend** : React, Vite, Tailwind CSS
- **Gestionnaire de paquets** : UV