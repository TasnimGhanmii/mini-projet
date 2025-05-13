
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import "./App.css"
import DisponibilitePage from './pages/DisponibilitePage';
import Header from './components/Header';



function App() {
  return (

    <div>
     
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/disponibilite" element={<DisponibilitePage />} />
        
      </Routes>
    </BrowserRouter>
    </div>
  );
}


export default App;
