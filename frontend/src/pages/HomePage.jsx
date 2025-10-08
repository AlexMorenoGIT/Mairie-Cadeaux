import {DataTable} from "../component/table.jsx";

export function HomePage({ onNavigate }) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-10 px-6">
            <div className="max-w-7xl mx-auto space-y-10">
                <div className="bg-white rounded-2xl shadow-lg p-8 flex flex-col md:flex-row items-center justify-between gap-6">
                    <div className="text-center md:text-left">
                        <h1 className="text-4xl font-bold text-gray-900 mb-2">🏠 Gestion des Foyers</h1>
                        <p className="text-gray-600">Bienvenue sur l'application de gestion des foyers</p>
                    </div>
                    <div className="flex flex-col sm:flex-row gap-4 w-full md:w-auto">
                        <button
                            onClick={() => onNavigate("homes")}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
                        >
                            Voir la liste des foyers →
                        </button>
                        <button
                            onClick={() => onNavigate("add-home")}
                            className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
                        >
                            Ajouter un foyer +
                        </button>
                    </div>
                </div>

                <DataTable
                    apiUrl="http://localhost:5001/api/homes/eligible"
                    title="Foyers éligibles"
                    emptyMessage="Aucun foyer éligible trouvé"
                />
            </div>
        </div>
    );
}
