import React, { useState } from 'react';
import './UploadPage.css';
import { useNavigate } from 'react-router-dom';
import { ArrowRight,ArrowLeft } from 'lucide-react';
import Header from '../components/Header';

const UploadPage: React.FC = () => {
  const [fileName, setFileName] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileName(file.name);
      // Tu peux traiter le fichier ici avec SheetJS par exemple si besoin
    }
  };

  const handleUpload = () => {
    if (!fileName) {
      alert('Veuillez sélectionner un fichier Excel.');
      return;
    }
    alert(`Fichier ${fileName} importé avec succès !`);
  };

  return (
    <div>
      <Header></Header>
    <div className="upload-container">
      <div className="upload-box">
        <h2>Importer un fichier Excel</h2>

        <div className="upload-form">
          <label htmlFor="excelFile" className="upload-label">
            Sélectionner un fichier Excel :
          </label>
          <input
            type="file"
            id="excelFile"
            accept=".xlsx, .xls"
            onChange={handleFileChange}
          />
          {fileName && <p className="file-name">Fichier sélectionné : {fileName}</p>}
        </div>

        <button className="upload-button" onClick={handleUpload}>
          Importer
        </button>

        <div className="groupbtn">
        <button className="arrow-button" onClick={() => navigate(-1)}>
          <ArrowLeft size={20} /> 
        </button>
        <button className="arrow-button" onClick={() => navigate("/disponibilite")}>
          <ArrowRight size={20} /> 
        </button>
        </div>
      </div>
    </div>
    </div>
  );
};

export default UploadPage;
