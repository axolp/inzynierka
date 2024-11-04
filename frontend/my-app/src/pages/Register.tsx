import React, { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/login.css";

export const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [repassword, setRepassword] = useState("");

  function handleSubmit() {
    console.log(email, password);
  }
  return (
    <div>
      <nav>
        <a href="#">
          <img src="images/logo.svg" alt="logo" />
        </a>
      </nav>
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
            <label>Email or phone number</label>
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
