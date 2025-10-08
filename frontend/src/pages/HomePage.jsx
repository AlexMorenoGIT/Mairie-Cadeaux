export function HomePage({ onNavigate }) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
            <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                    🏠 Gestion des Foyers
                </h1>
                <p className="text-gray-600 mb-8">
                    Bienvenue sur l'application de gestion des foyers
                </p>
                <button
                    onClick={() => onNavigate('homes')}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-6 rounded-lg transition duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                    Voir la liste des foyers →
                </button>
                <button
                    onClick={() => onNavigate('add-home')}
                    className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-4 px-6 rounded-lg transition duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                    Ajouter un foyer +
                </button>
            </div>
        </div>
    );
}