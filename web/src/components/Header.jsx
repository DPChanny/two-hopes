import React from "react";
import "../styles/Header.css";
import logo from "../assets/logo.png";
import { useNavigate } from "react-router-dom";

const Header = () => {
  const navigate = useNavigate();

  return (
    <header>
      <img
        src={logo}
        alt="header-logo"
        className="header-logo"
        onClick={() => navigate("/")}
      />
    </header>
  );
};

export default Header;
