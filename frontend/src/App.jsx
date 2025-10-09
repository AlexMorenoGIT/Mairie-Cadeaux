import { useState } from 'react';
import { HomePage } from './pages/HomePage.jsx';
import { HomesListPage } from './pages/HomeListPage.jsx';
import { HomeAddPage } from './pages/HomeAddPage.jsx';
import {ShipmentsList} from "./pages/ShipmentsList.jsx";

export default function App() {
    const [currentPage, setCurrentPage] = useState('home');

    const navigateTo = (page) => {
        setCurrentPage(page);
    };

    switch (currentPage) {
        case 'shipments':
            return <ShipmentsList onNavigate={navigateTo} />;
        case 'homes':
            return <HomesListPage onNavigate={navigateTo} />;
        case 'add-home':
            return <HomeAddPage onNavigate={navigateTo} />;
        case 'home':
        default:
            return <HomePage onNavigate={navigateTo} />;
    }
}