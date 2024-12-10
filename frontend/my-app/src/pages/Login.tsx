import React, { useState } from "react";
import { Route, Link, useNavigate } from "react-router-dom";
import "../styles/login.css";
export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault(); // Zapobiega odświeżeniu strony

    try {
      // Wysyłanie danych do backendu Django
      const response = await fetch("http://127.0.0.1:8000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      if (response.ok) {
        // Otrzymanie odpowiedzi JSON z backendu
        const data = await response.json();
        console.log("Zalogowano pomyślnie:", data);
        localStorage.setItem("user_id", data.user_id);

        // Przekierowanie do /flashcards
        navigate("/flashcards");
      } else {
        // Obsługa błędów logowania
        console.error("Błąd logowania:", response.status);
        alert("Logowanie nie powiodło się. Sprawdź dane logowania.");
      }
    } catch (error) {
      // Obsługa błędów sieciowych
      console.error("Błąd sieci:", error);
      alert("Wystąpił problem z połączeniem z serwerem.");
    }
  }

  return (
    <div>
      <nav>
        <a href="#"></a>
      </nav>
      <div className="form-wrapper">
        <h2>Sign In</h2>
        <form action="#">
          <div className="form-control">
            <input
              type="text"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
            <label>Email</label>
          </div>
          <div className="form-control">
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
            <label>Password</label>
          </div>
          <button type="submit" onClick={handleSubmit}>
            Sign In
          </button>
          <div className="form-help">
            <div className="remember-me">
              <input type="checkbox" id="remember-me" />
              <label htmlFor="remember-me">Remember me</label>
            </div>
            <a href="#">Need help?</a>
          </div>
        </form>
        <p>
          <p>
            New to MemApex? <Link to="/register">Sign up now</Link>
          </p>
        </p>
        <small>
          This page is protected by Google reCAPTCHA to ensure you're not a bot.
          <a href="#">Learn more.</a>
        </small>
      </div>
    </div>
  );
};
