import {useEffect, useState} from "react";

export function DataTable({
                              apiUrl,
                              title = "Tableau de données",
                              emptyMessage = "Aucune donnée disponible",
                          }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadData();
    }, [apiUrl]);

    const loadData = async () => {
        try {
            setLoading(true);
            const response = await fetch(apiUrl);
            if (!response.ok) throw new Error("Erreur lors du chargement des données");

            const result = await response.json();
            setData(Array.isArray(result) ? result : []);
            setError(null);
        } catch (err) {
            console.error("Erreur:", err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => new Date(dateString).toLocaleDateString("fr-FR");

    const columns = [
        {key: "name", header: "Nom"},
        {key: "firstname", header: "Prénom"},
        {
            key: "birth_date",
            header: "Date de naissance",
            render: (value) => <span className="text-sm text-gray-500">{formatDate(value)}</span>,
        },
        {
            key: "email",
            header: "Email",
            render: (value) => <span className="text-sm text-blue-600">{value}</span>,
        },
        {
            key: "postal_address",
            header: "Adresse",
            render: (value) => <span className="text-sm text-gray-500 max-w-xs truncate">{value}</span>,
        },
        {
            key: "created_at",
            header: "Créé le",
            render: (value) => <span className="text-sm text-gray-500">{formatDate(value)}</span>,
        },
    ];

    // --- États spéciaux ---
    if (loading) {
        return (
            <div className="flex justify-center py-10">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Chargement des données...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto text-center">
                <h2 className="text-red-800 font-bold text-xl mb-2">❌ Erreur</h2>
                <p className="text-red-600 mb-4">{error}</p>
                <button
                    onClick={loadData}
                    className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
                >
                    Réessayer
                </button>
            </div>
        );
    }

    // --- Affichage principal ---
    return (
        <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="mb-6 flex items-center justify-between flex-wrap gap-2">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-1">{title}</h2>
                    <p className="text-gray-600">
                        {data.length} foyer{data.length > 1 ? "s" : ""} trouvé{data.length > 1 ? "s" : ""}
                    </p>
                </div>
                <button
                    onClick={loadData}
                    className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition"
                >
                    ↻ Actualiser
                </button>
            </div>

            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                    <tr>
                        {columns.map((col) => (
                            <th
                                key={col.key}
                                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                {col.header}
                            </th>
                        ))}
                    </tr>
                    </thead>

                    <tbody className="bg-white divide-y divide-gray-200">
                    {data.length === 0 ? (
                        <tr>
                            <td
                                colSpan={columns.length}
                                className="px-6 py-8 text-center text-gray-500"
                            >
                                {emptyMessage}
                            </td>
                        </tr>
                    ) : (
                        data.map((row, idx) => (
                            <tr key={idx} className="hover:bg-gray-50 transition">
                                {columns.map((col) => (
                                    <td
                                        key={col.key}
                                        className="px-6 py-4 whitespace-nowrap"
                                    >
                                        {col.render
                                            ? col.render(row[col.key], row)
                                            : (
                                                <div className="text-sm text-gray-900">
                                                    {row[col.key]}
                                                </div>
                                            )}
                                    </td>
                                ))}
                            </tr>
                        ))
                    )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
