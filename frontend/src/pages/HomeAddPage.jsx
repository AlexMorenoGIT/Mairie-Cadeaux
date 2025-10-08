import { useState } from "react";

export function HomeAddPage({ onNavigate }) {
    const [formData, setFormData] = useState({
        name: "",
        firstname: "",
        birth_date: "",
        email: "",
        postal_address: "",
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            console.log(JSON.stringify(formData));
            const response = await fetch("http://localhost:5001/api/homes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error(`Erreur serveur : ${response.status}`);
            }

            const data = await response.json();
            console.log("✅ Foyer ajouté avec succès :", data);

            setFormData({
                name: "",
                firstname: "",
                birth_date: "",
                email: "",
                postal_address: "",
            });
            onNavigate("homes");

        } catch (error) {
            console.error("❌ Erreur lors de l'ajout du foyer :", error);
            alert("Une erreur est survenue lors de l'envoi du formulaire.");
        }
    };


    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-6">
            <div className="w-full max-w-2xl bg-white shadow-xl rounded-2xl p-10 border border-gray-200">
                <h2 className="text-2xl font-bold text-gray-800 mb-8 text-center">
                    Ajouter un élément
                </h2>
                <button
                    onClick={() => onNavigate('home')}
                    className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
                >
                    ← Retour
                </button>

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
                    <div className="pt-4 text-center">
                        <button
                            type="submit"
                            className="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 transition-colors duration-200"
                        >
                            Envoyer
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
