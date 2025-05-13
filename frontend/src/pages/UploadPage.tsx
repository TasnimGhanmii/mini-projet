import React, { useState } from 'react';
import './UploadPage.css';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, ArrowLeft } from 'lucide-react';
import Header from '../components/Header';
import axios from 'axios';

const UploadPage:React.FC =()=>{
  const apiUrl = 'http://127.0.0.1:8000/playground/affecter-profs/';

async function affecterProfesseurs() {
    try {
        // Effectuer la requête POST pour appeler la fonction Django
        const response = await axios.get(apiUrl,{headers:{
                'Content-Type': 'application/json',  // Définir le type de contenu
                
            }}
        );

        // Afficher la réponse du serveur
        console.log('Réponse:', response.data);
    } catch (error) {
        console.error('Erreur lors de la requête:', error);
    }
}
async function genererPdf() {
  // Appelez d'abord la fonction affecterProfesseurs pour attendre qu'elle soit terminée
  await affecterProfesseurs();

  // Une fois que la fonction affecterProfesseurs est terminée, vous pouvez exécuter la requête GET
  try {
    const response4 = await axios({
      url: 'http://127.0.0.1:8000/playground/generer-pdf/', 
      method: 'GET',
      responseType: 'blob', 
    });

      console.log('Réponse du PDF:', response4.data);
      const blob = response4.data;
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'affectations_enseignants.pdf';  // Nom du fichier à télécharger
      document.body.appendChild(link);
      link.click();  // Simule le clic sur le lien pour télécharger le fichier
      document.body.removeChild(link);
  } catch (error) {
      console.error('Erreur lors de la génération du PDF:', error);
  }
}

  const [fileNames, setFileNames] = useState<(string | null)[]>([null, null, null]);
  const [files, setFiles] = useState<(File | null)[]>([null, null, null]);
  
  const navigate = useNavigate();

  // Fonction pour gérer le changement des fichiers
  const handleFileChange = (index: number) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setFileNames((prevFileNames) => {
        const newFileNames = [...prevFileNames];
        newFileNames[index] = file.name;
        return newFileNames;
      });
      setFiles((prevFiles) => {
        const newFiles = [...prevFiles];
        newFiles[index] = file;
        return newFiles;
      });
    }
  }
  // Fonction pour gérer l'upload
  const handleUpload = async () => {
    if (files.some((file) => file === null)) {
      alert('Veuillez sélectionner tous les fichiers Excel.');
      return;
    }

    try {
      // FormData pour envoyer les fichiers avec Axios
      const formData1 = new FormData();
      formData1.append('fichier_excel', files[0] as File);
      const formData2 = new FormData();
      formData2.append('fichier_excel', files[1] as File);
      const formData3 = new FormData();
      formData3.append('fichier_excel', files[2] as File);

      // Envoi des fichiers vers le backend
      const response1 = await axios.post(
        'http://127.0.0.1:8000/playground/importenseignants/',
        formData1,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      const response2 = await axios.post(
        'http://127.0.0.1:8000/playground/importsessions/',
        formData2,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      const response3 = await axios.post(
        'http://127.0.0.1:8000/playground/importdevoirs/',
        formData3,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      
    genererPdf()
      alert('Fichiers importés avec succès !');
    } catch (error) {
      console.error('Erreur lors de l\'envoi des fichiers:', error);
      alert('Une erreur est survenue lors de l\'importation des fichiers.');
    }
  };

  return (
    <div>
      <Header />
      <div className="upload-container">
        <div className="upload-box">
          <h2>Importer des fichiers Excel</h2>

          <div className="upload-form">
            <label htmlFor="excelFile1" className="upload-label">
              selectionner le fichier des enseignants :
            </label>
            <input
              type="file"
              id="excelFile1"
              accept=".xlsx, .xls"
              onChange={handleFileChange(0)}
            />
            {fileNames[0] && <p className="file-name">Fichier 1 sélectionné : {fileNames[0]}</p>}

            <label htmlFor="excelFile2" className="upload-label">
              Sélectionner le fichier des sessions:
            </label>
            <input
              type="file"
              id="excelFile2"
              accept=".xlsx, .xls"
              onChange={handleFileChange(1)}
            />
            {fileNames[1] && <p className="file-name">Fichier 2 sélectionné : {fileNames[1]}</p>}

            <label htmlFor="excelFile3" className="upload-label">
              Sélectionner le fichiers des devoirs:
            </label>
            <input
              type="file"
              id="excelFile3"
              accept=".xlsx, .xls"
              onChange={handleFileChange(2)}
            />
            {fileNames[2] && <p className="file-name">Fichier 3 sélectionné : {fileNames[2]}</p>}
          </div>

          <button className="upload-button" onClick={handleUpload}>
            Générer
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
