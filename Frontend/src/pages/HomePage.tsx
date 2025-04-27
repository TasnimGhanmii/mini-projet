import React from "react";
import { useNavigate } from "react-router-dom";  // Utilisation de useNavigate pour la redirection
import Header from "../components/Header";



function Homepage() {
  const navigate = useNavigate();
  const handleGererDisponibilite = () => {
    navigate("/disponibilite");  // Rediriger vers la page Gérer Disponibilité
  };

  const handleGenererSurveillance = () => {
    navigate("/upload");  // Rediriger vers la page Générer Surveillance
  };

  
  return (
    <div className="homepage">
      <Header></Header>
      <div className="buttons-container">
        <button className="action-button" onClick={handleGererDisponibilite}>
          Gérer disponibilité
        </button>
        <button className="action-button" onClick={handleGenererSurveillance}>
          Générer surveillance
        </button>
      </div>
    </div>
  );
}

export default Homepage;