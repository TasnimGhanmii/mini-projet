import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { LogOut, ArrowLeft, Search, ArrowRight } from "lucide-react";

import "./DisponibilitePage.css";
import Header from "../components/Header";

const days = ["Jour 1", "Jour 2", "Jour 3", "Jour 4"];
const sessions = ["S1", "S2", "S3", "S4"];

const DisponibilitePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [checked, setChecked] = useState<boolean[][]>(
    Array(days.length)
      .fill(null)
      .map(() => Array(sessions.length).fill(false))
  );

  const navigate = useNavigate();

  const toggleCheck = (dayIndex: number, sessionIndex: number) => {
    const newChecked = [...checked];
    newChecked[dayIndex][sessionIndex] = !newChecked[dayIndex][sessionIndex];
    setChecked(newChecked);
  };

  const handleSubmit = () => {
    const disponibilites = days.map((_, dayIndex) => {
      return sessions.map((_, sessionIndex) => checked[dayIndex][sessionIndex]);
    });
    console.log("Disponibilités soumises :", disponibilites);
    alert("Disponibilité envoyée !");
  };

  return (
    <div>
      <Header></Header>
      <div className="dispo-container">
        <div className="dispo-box">
          

          
          <div className="dispo-search">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Nom du professeur"
            />
            <Search className="search-icon" />
          </div>

          
          <h2 className="dispo-title">Disponibilité</h2>
          <div className="dispo-grid">
            <div></div>
            {days.map((day, index) => (
              <div key={index} className="grid-header">
                {day}
              </div>
            ))}
            {sessions.map((session, sIdx) => (
              <React.Fragment key={sIdx}>
                <div className="grid-row">{session}</div>
                {days.map((_, dIdx) => (
                  <div key={`${dIdx}-${sIdx}`} className="grid-checkbox">
                    <input
                      type="checkbox"
                      checked={checked[dIdx][sIdx]}
                      onChange={() => toggleCheck(dIdx, sIdx)}
                    />
                  </div>
                ))}
              </React.Fragment>
            ))}
          </div>

          
          <div className="dispo-submit">
            <button onClick={handleSubmit}>Soumettre</button>
          </div>

          
          <div className="groupbtn">

          <button onClick={() => navigate(-1)} className="arrow-button">
            <ArrowLeft size={20} />
          </button>
          <button className="arrow-button" onClick={() => navigate("/upload")}>
          <ArrowRight size={20} /> 
        </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DisponibilitePage;
