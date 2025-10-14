import { useState } from 'react';
import { HomePage } from './pages/HomePage.jsx';
import { HomesListPage } from './pages/HomeListPage.jsx';
import { HomeAddPage } from './pages/HomeAddPage.jsx';
import { ShipmentsList } from "./pages/ShipmentsList.jsx";
import { HomeEditPage } from "./pages/HomeEditPage.jsx";

export default function App() {
    const [route, setRoute] = useState({ name: 'home', params: null });

    const navigateTo = (name, params = null) => setRoute({ name, params });

    switch (route.name) {
        case 'shipments':
            return <ShipmentsList onNavigate={navigateTo} />;
        case 'homes':
            return <HomesListPage onNavigate={navigateTo} />;
        case 'add-home':
            return <HomeAddPage onNavigate={navigateTo} />;

        case 'edit-home':
            return <HomeEditPage onNavigate={navigateTo} params={route.params} />;

        case 'home':
        default:
            return <HomePage onNavigate={navigateTo} />;
    }
}
