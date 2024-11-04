import React, { useState } from "react";
import { Route, Link, useNavigate } from "react-router-dom";
import "../styles/login.css";
export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleSubmit() {
    console.log(email, password);
    navigate("/flashcards");
    console.log("dlaczego nie przekierowalem?");
  }

  return (
    <div>
      <nav>
        <a href="#">
          <img src="images/logo.svg" alt="logo" />
        </a>
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
