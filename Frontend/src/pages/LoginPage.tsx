import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Importation de useNavigate au lieu de useHistory
import Header from "../components/Header";


function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate(); // Utilisation de useNavigate

  // Fonction de soumission du formulaire
  const handleSubmit =(e)=> {
    e.preventDefault();

    // Vérification de l'email et du mot de passe
    if (email === "admin" && password === "0000") {
      setError('');
      navigate("/Home"); // Utilisation de navigate pour rediriger
    } else {
      setError("Email ou mot de passe incorrect");
    }
  };

  return (
    <div className="login-container">
   
      <div className="login-box">
        
        <div className="icon-container">
          <svg
            className="icon"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
            />
          </svg>
        </div>
        <h2 className="welcome-text">Bienvenu(e)</h2>
        <p className="sub-text">Veuillez saisir vos paramètres d'accès</p>

        <form className="login-form" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Nom d'utilisateur"
            className="input-field"
            value={email}
            onChange={(e) => setEmail(e.target.value)} // Mise à jour de l'email
          />
          <input
            type="password"
            placeholder="Mot de passe"
            className="input-field"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Mise à jour du mot de passe
          />
          <button
            type="submit"
            className="submit-btn"
          >
            Se connecter
          </button>
        </form>

        {/* Message d'erreur */}
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
}

export default LoginPage;