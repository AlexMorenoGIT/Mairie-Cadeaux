import {DataTable} from "../component/table.jsx";

export function ShipmentsList({ onNavigate }) {
    const shipmentsColumns = [
        {
            key: "id",
            header: "ID",
            render: (value) => (
                <span className="text-xs text-gray-500 font-mono">
                    {value}
                </span>
            ),
        },
        {
            key: "home_id",
            header: "Foyer",
            render: (value) => (
                <span className="text-xs text-gray-500 font-mono">
                    {value}
                </span>
            ),
        },
        {
            key: "gift_id",
            header: "Cadeau",
            render: (value) => (
                <span className="text-xs text-gray-500 font-mono">
                    {value}
                </span>
            ),
        },
        {
            key: "status",
            header: "Statut",
            render: (value) => {
                const statusColors = {
                    EN_ATTENTE: "bg-yellow-100 text-yellow-800",
                    EXPEDIE: "bg-blue-100 text-blue-800",
                    RECU: "bg-green-100 text-green-800",
                };
                return (
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[value] || "bg-gray-100 text-gray-800"}`}>
                        {value}
                    </span>
                );
            },
        },
        {
            key: "created_at",
            header: "Date de création",
            render: (value) => (
                <span className="text-sm text-gray-500">
                    {new Date(value).toLocaleDateString("fr-FR")}
                </span>
            ),
        },
    ];
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
                    apiUrl="http://localhost:5001/api/shipments"
                    title="Tous les foyers"
                    emptyMessage="Aucun foyer enregistré"
                    columns={shipmentsColumns}
                />
            </div>
        </div>
    );
}
