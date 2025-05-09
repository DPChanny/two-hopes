import React from "react";
import logo from "../assets/welcome_logo.png";
import "../styles/Welcome.css";
import { Link } from "react-router-dom";

const Welcome = () => {
  return (
    <div className="welcome">
      <div className="welcome-logo">
        <img src={logo} alt="welcome-logo" className="welcome-logo-img" />
      </div>
      <Link to="/main" className="welcome-btn">
        나만의 작물 키우러 가기
      </Link>
    </div>
  );
};

export default Welcome;
