
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate(); // Initialisation de useNavigate

  const handleDeconnexion = () => {
    navigate("/");
  };
  return (
    <header className="header">
      <img src="logoissat.jpeg" alt="Logo" className="logo" />
      <button className="deconnexion" onClick={handleDeconnexion}>
        ⏏ Se déconnecter
      </button>{" "}
      {/* Déconnexion */}
    </header>
  );
};

export default Header;
