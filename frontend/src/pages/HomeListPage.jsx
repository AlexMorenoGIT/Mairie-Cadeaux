import {DataTable} from "../component/table.jsx";

export function HomesListPage({ onNavigate }) {
    return (
        <div className="min-h-screen bg-gray-50 py-8 px-4">
            <div className="max-w-7xl mx-auto">
                <div className="mb-8 flex items-center justify-between">
                    <h1 className="text-4xl font-bold text-gray-900">Liste des Foyers</h1>
                    <button
                        onClick={() => onNavigate("home")}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg transition"
                    >
                        ← Retour
                    </button>
                </div>

                <DataTable
                    apiUrl="http://localhost:5001/api/homes"
                    title="Tous les foyers"
                    emptyMessage="Aucun foyer enregistré"
                />
            </div>
        </div>
    );
}
