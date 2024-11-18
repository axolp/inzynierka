import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { IpcRendererEvent } from "electron";
//const { ipcRenderer } = window.require("electron") as typeof import("electron");
const { ipcRenderer } = window.require("electron");
const logged_user_id = localStorage.getItem("user_id");

interface Flashcard {
  characters: "你好";
  easiness_factor: 2.5;
  id: 1;
  last_repetition_date: "1969-07-20";
  meaning: "hi";
  next_repetition_date: "1969-07-20";
  repetition_number: 0;
}

export const Flashcards = () => {
  const [flashcards, setFlashcards] = useState<Flashcard[]>([]);
  const [flashcardNumber, setFlashcard_number] = useState(0);
  const [revealFlashcards, setReveal] = useState(false);

  async function updateFlashcard(answer: string) {
    try {
      // Wysyłanie danych do backendu Django
      const response = await fetch(
        "http://127.0.0.1:8000/api/updateFlashcards",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            id: flashcards[flashcardNumber].id,
            user_answer: answer,
            pupil_dilatation: 15,
          }),
        }
      );

      if (response.ok) {
        // Otrzymanie odpowiedzi JSON z backendu
        const data = await response.json();
        //console.log("Otrzymano fiszki:", data);
        console.log("zaktualizowan fiszek na backend");

        // Przekierowanie do /flashcards
      } else {
        // Obsługa błędów logowania
        console.error("Błąd w aktualizowaniu fiszek:", response.status);
        alert("nie zaktualizowano fiszek");
      }
    } catch (error) {
      // Obsługa błędów sieciowych
      console.error("Błąd sieci:", error);
      alert("Wystąpił problem z połączeniem z serwerem.");
    }
  }
  async function getFlashcards() {
    //event.preventDefault(); // Zapobiega odświeżeniu strony
    try {
      // Wysyłanie danych do backendu Django
      const response = await fetch("http://127.0.0.1:8000/api/flashcards", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: logged_user_id,
        }),
      });

      if (response.ok) {
        // Otrzymanie odpowiedzi JSON z backendu
        const data = await response.json();
        //console.log("Otrzymano fiszki:", data);
        setFlashcards(data.flashcards);
        console.log(flashcards);

        // Przekierowanie do /flashcards
      } else {
        // Obsługa błędów logowania
        console.error("Błąd otrzymania fiszek:", response.status);
        alert("nie trzyamno fiszek");
      }
    } catch (error) {
      // Obsługa błędów sieciowych
      console.error("Błąd sieci:", error);
      alert("Wystąpił problem z połączeniem z serwerem.");
    }
  }

  useEffect(() => {
    getFlashcards();
  }, []);

  useEffect(() => {
    console.log(flashcards[0]);
  }, [flashcards]);

  // useEffect(() => {}, [flashcardNumber]);

  useEffect(() => {
    // Uruchamianie programu Python przy załadowaniu komponentu
    ipcRenderer.send("start-python");
    console.log("Powinienem uruchomic pythona");

    // Nasłuchiwanie na dane z programu Python
    ipcRenderer.on(
      "python-data",
      (event: Electron.IpcRendererEvent, data: String) => {
        console.log("Dane z programu Python:", data);
      }
    );

    // Czyszczenie przy odmontowaniu komponentu
    return () => {
      ipcRenderer.send("stop-python");
      ipcRenderer.removeAllListeners("python-data");
    };
  }, []);

  return (
    <div>
      STRONA NA FISZKI!!
      {flashcards[flashcardNumber] ? (
        revealFlashcards ? (
          <p>{flashcards[flashcardNumber].meaning}</p>
        ) : (
          <p>{flashcards[flashcardNumber].characters}</p>
        )
      ) : (
        <p>Czekam na fiszki</p>
      )}
      ;<button onClick={() => setReveal(true)}>sprawdz</button>
      <button
        onClick={() => {
          setReveal(false);
          setFlashcard_number(flashcardNumber + 1);
          updateFlashcard("very easy");
        }}
      >
        very easy
      </button>
      <button
        onClick={() => {
          setReveal(false);
          setFlashcard_number(flashcardNumber + 1);
          updateFlashcard("easy");
        }}
      >
        latwe
      </button>
      <button
        onClick={() => {
          setReveal(false);
          setFlashcard_number(flashcardNumber + 1);
          updateFlashcard("medium");
        }}
      >
        srednie
      </button>
      <button
        onClick={() => {
          setReveal(false);
          setFlashcard_number(flashcardNumber + 1);
          updateFlashcard("hard");
        }}
      >
        trudne
      </button>
      <button
        onClick={() => {
          setReveal(false);
          setFlashcard_number(flashcardNumber + 1);
          updateFlashcard("very hard");
        }}
      >
        bardzo trudne
      </button>
      <button
        onClick={() => {
          setReveal(false);
          setFlashcard_number(flashcardNumber + 1);
          updateFlashcard("black out");
        }}
      >
        black out
      </button>
    </div>
  );
};
