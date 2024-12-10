import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/login.css";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [repassword, setRepassword] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/api/register", {
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
        const data = await response.json();
        console.log("Rejestracja pomyślna:", data);
        navigate("/");
        alert("Konto zostało utworzone pomyślnie!");
      } else {
        const errorData = await response.json();
        alert(errorData.error || "Rejestracja nie powiodła się.");
      }
    } catch (error) {
      console.error("Błąd rejestracji:", error);
      alert("Wystąpił problem z połączeniem z serwerem.");
    }
  }
  return (
    <div>
      <nav></nav>
      <div className="form-wrapper">
        <h2>Register</h2>
        <form>
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
          <div className="form-control">
            <input
              type="password"
              value={repassword}
              onChange={(event) => setRepassword(event.target.value)}
              required
            />
            <label>Repeat Password</label>
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
          Already have an account in MemApex? <Link to="/">Log in now</Link>
        </p>
        <small>
          This page is protected by Google reCAPTCHA to ensure you're not a bot.
          <a href="#">Learn more.</a>
        </small>
      </div>
    </div>
  );
};
