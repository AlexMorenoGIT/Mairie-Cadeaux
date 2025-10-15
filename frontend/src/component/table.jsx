import {useEffect, useState} from "react";

export function DataTable({
                              apiUrl,
                              title = "Tableau de données",
                              emptyMessage = "Aucune donnée disponible",
                              run = false,
                              onNavigate,
                              columns,
                              withActions = false,
                              onEdit,
                              onDeleted,
                              getRowId = (row) => row.id,
                          }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [attributions, setAttributions] = useState(false);
    const [error, setError] = useState(null);
    const [busyId, setBusyId] = useState(null);

    useEffect(() => {
        loadData();
        if (run) {
            checkAttributionToday();
        }
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
    const checkAttributionToday = async () => {
        try {
            const response = await fetch('http://localhost:5001/api/shipments');
            if (!response.ok) throw new Error("Erreur lors du chargement de la vérification de l'attribution");

            const result = await response.json();
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const attributionToday = result.some(shipment => {
                const shipmentDate = new Date(shipment.created_at);
                shipmentDate.setHours(0, 0, 0, 0);
                console.log(shipmentDate, today);
                return shipmentDate.getTime() === today.getTime();
            });

            setAttributions(attributionToday);
        } catch (error) {
            console.error("Erreur lors de la vérification:", error);
        }
    };

    const runAttribution = async () => {
        try {
            for (let i = 0; i < data.length; i++) {
                const response = await fetch(`http://localhost:5001/api/shipments/${data[i]['id']}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    }
                })
                if (!response.ok) {
                    throw new Error('Erreur lors du lancement de l\'attribution')
                }
            }
            alert("Attributions réussies")
            window.location.reload()
        } catch (error) {
            console.error("Erreur:", error);
            setError(error.message);
        }
    }

    const formatDate = (dateString) => {
        if (!dateString) return "-";
        return new Date(dateString).toLocaleDateString("fr-FR");
    };

    // Colonnes par défaut pour les foyers (homes)
    const defaultColumns = [
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
            key: 'gift',
            header: "Cadeau",
            render: (value) => <span className="text-sm text-gray-500">{value?.name || "-"}</span>,
        },
        {
            key: "created_at",
            header: "Créé le",
            render: (value) => <span className="text-sm text-gray-500">{formatDate(value)}</span>,
        },
    ];

    const columnsToUse = columns || defaultColumns;

    const handleEdit = (row) => {
        if (onEdit) {
            onEdit(row);
            return;
        }
        if (onNavigate) {
            onNavigate("edit-home", { id: getRowId(row), row });
        } else {
            alert("Aucune action d’édition configurée.");
        }
    };

    const handleDelete = async (row) => {
        const id = getRowId(row);
        if (!id) return;

        const ok = confirm(`Supprimer le foyer #${id} ?`);
        if (!ok) return;

        try {
            setBusyId(id);
            const res = await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
            if (!res.ok) {
                const body = await res.json().catch(() => ({}));
                throw new Error(body?.error || "Suppression impossible");
            }
            // Optimistic update
            setData((prev) => prev.filter((r) => getRowId(r) !== id));
            if (onDeleted) onDeleted(id);
        } catch (e) {
            console.error(e);
            alert(e.message || "Erreur lors de la suppression");
        } finally {
            setBusyId(null);
        }
    };

    const finalColumns = withActions
        ? [
            ...columnsToUse,
            {
                key: "__actions",
                header: "Actions",
                render: (_v, row) => (
                    <div className="flex items-center gap-2 justify-end">
                        <button
                            onClick={() => handleEdit(row)}
                            className="inline-flex items-center gap-1 bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 px-3 py-1.5 rounded-lg text-sm"
                            title="Éditer"
                        >
                            Éditer
                        </button>
                        <button
                            onClick={() => handleDelete(row)}
                            disabled={busyId === getRowId(row)}
                            className={`inline-flex items-center gap-1 ${
                                busyId === getRowId(row)
                                    ? "bg-red-300 cursor-not-allowed"
                                    : "bg-red-600 hover:bg-red-700"
                            } text-white px-3 py-1.5 rounded-lg text-sm`}
                            title="Supprimer"
                        >
                            Supprimer
                        </button>
                    </div>
                ),
            },
        ]
        : columnsToUse;

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
                        {data.length} élément{data.length > 1 ? "s" : ""} trouvé{data.length > 1 ? "s" : ""}
                    </p>
                </div>
                <div className="flex flex-wrap gap-2">
                    {run && onNavigate && (
                        <>
                            <button
                                onClick={() => onNavigate("shipments")}
                                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
                            >
                                Voir la liste des attributions effectués →
                            </button>
                            {data.length > 0 && attributions === false && (
                                <button
                                    onClick={runAttribution}
                                    className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 shadow-md hover:shadow-lg"
                                >
                                    Lancer les attributions
                                </button>
                            )
                            }

                        </>
                    )}
                    <button
                        onClick={loadData}
                        className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-lg transition"
                    >
                        ↻ Actualiser
                    </button>
                </div>
            </div>

            <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                    <tr>
                        {finalColumns.map((col) => (
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
                            <td colSpan={finalColumns.length} className="px-6 py-8 text-center text-gray-500">
                                {emptyMessage}
                            </td>
                        </tr>
                    ) : (
                        data.map((row, idx) => (
                            <tr key={getRowId(row) ?? idx} className="hover:bg-gray-50 transition">
                                {finalColumns.map((col) => (
                                    <td key={col.key} className="px-6 py-4 whitespace-nowrap">
                                        {col.render ? col.render(row[col.key], row) : (
                                            <div className="text-sm text-gray-900">
                                                {row[col.key] ?? "-"}
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