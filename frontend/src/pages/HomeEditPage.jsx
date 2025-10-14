// EditHomePage.jsx
import { useEffect, useState } from "react";

export function HomeEditPage({ onNavigate, params }) {
    const homeId = params?.id;
    const initialRow = params?.row;

    const [formData, setFormData] = useState({
        name: "",
        firstname: "",
        birth_date: "",
        email: "",
        postal_address: "",
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    const toInputDate = (value) => {
        if (!value) return "";
        return String(value).slice(0, 10);
    };

    // Charge les données si pas fournies, sinon hydrate directement
    useEffect(() => {
        const hydrate = (row) => {
            setFormData({
                name: row?.name ?? "",
                firstname: row?.firstname ?? "",
                birth_date: toInputDate(row?.birth_date),
                email: row?.email ?? "",
                postal_address: row?.postal_address ?? "",
            });
            setLoading(false);
            setError(null);
        };

        if (initialRow) {
            hydrate(initialRow);
            return;
        }

        // Sinon on va chercher l'item
        const fetchOne = async () => {
            try {
                setLoading(true);
                const res = await fetch(`http://localhost:5001/api/homes/${homeId}`);
                if (!res.ok) {
                    const body = await res.json().catch(() => ({}));
                    throw new Error(body?.error || `Impossible de charger le foyer #${homeId}`);
                }
                const data = await res.json();
                hydrate(data);
            } catch (e) {
                setError(e.message);
                setLoading(false);
            }
        };

        if (!homeId) {
            setError("Aucun identifiant fourni.");
            setLoading(false);
        } else {
            fetchOne();
        }
    }, [homeId, initialRow]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((s) => ({ ...s, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!homeId) return;

        try {
            setSaving(true);
            setError(null);

            const res = await fetch(`http://localhost:5001/api/homes/${homeId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            if (!res.ok) {
                const body = await res.json().catch(() => ({}));
                throw new Error(body?.error || `Erreur serveur : ${res.status}`);
            }

            alert("✅ Modifications enregistrées");
            onNavigate?.("homes");
        } catch (e) {
            console.error(e);
            setError(e.message || "Une erreur est survenue");
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-gray-600">Chargement…</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-6">
            <div className="w-full max-w-2xl bg-white shadow-xl rounded-2xl p-10 border border-gray-200">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-2xl font-bold text-gray-800">
                        Éditer le foyer #{homeId}
                    </h2>
                    <button
                        onClick={() => onNavigate("homes")}
                        className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
                    >
                        ← Retour
                    </button>
                </div>

                {error && (
                    <div className="mb-4 p-3 rounded bg-red-50 text-red-700 border border-red-200">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Nom
                            </label>
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                                className="w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm p-2"
                                placeholder="Ex : Dupont"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Prénom
                            </label>
                            <input
                                type="text"
                                name="firstname"
                                value={formData.firstname}
                                onChange={handleChange}
                                required
                                className="w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm p-2"
                                placeholder="Ex : Marie"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Date de naissance
                        </label>
                        <input
                            type="date"
                            name="birth_date"
                            value={formData.birth_date}
                            onChange={handleChange}
                            required
                            className="w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm p-2"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Adresse email
                        </label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            className="w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm p-2"
                            placeholder="exemple@email.com"
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Adresse postale
                        </label>
                        <input
                            type="text"
                            name="postal_address"
                            value={formData.postal_address}
                            onChange={handleChange}
                            required
                            className="w-full rounded-lg border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 shadow-sm p-2"
                            placeholder="Ex : 12 rue des Lilas, 75000 Paris"
                        />
                    </div>

                    <div className="pt-4 flex items-center gap-3">
                        <button
                            type="button"
                            onClick={() => onNavigate("homes")}
                            className="bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-4 py-2 rounded-lg transition"
                            disabled={saving}
                        >
                            Annuler
                        </button>
                        <button
                            type="submit"
                            disabled={saving}
                            className={`px-6 py-3 text-white font-semibold rounded-lg shadow-md transition-colors duration-200 ${
                                saving ? "bg-indigo-300 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700"
                            }`}
                        >
                            {saving ? "Enregistrement…" : "Enregistrer"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
