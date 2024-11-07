import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useUser } from "../components/UserContext";

export const Flashcards = () => {
  const { userId } = useUser();
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/flashcards", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Pobrano fiszki dla obecnie zalogowanego użytkownika");
        console.log(data);
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    handleSubmit();
  }, [userId]);

  useEffect(() => {
    // Rozpoczynamy analizę obrazu z kamery po zamontowaniu komponentu
    if (window.electronAPI) {
      console.log("elektron api istnieje, spelnionbe")
      window.electronAPI.startAnalysis();
      console.log("analiza rozpoczeta")

      // Odbieranie wyników analizy z Electrona
      window.electronAPI.onAnalysisResult((result) => {
        console.log(result)
        setAnalysisResult(result); // Ustaw wynik analizy w stanie
        console.log(analysisResult);
      });
    }else{
      console.log("cos nie tak z electronAPI");
    }
  }, []);

  return (
    <div>
      <h2>STRONA NA FISZKI!!</h2>
      {analysisResult ? (
        <div>
          <p>Wynik analizy obrazu: {JSON.stringify(analysisResult)}</p>
        </div>
      ) : (
        <p>Analiza obrazu w toku...</p>
      )}
      <Link to="/">Powrót</Link>
    </div>
  );
};
