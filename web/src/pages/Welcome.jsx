import React from "react";
import logo from "../assets/logo.png";
import "../styles/Welcome.css";
import { Link } from "react-router-dom";

const Welcome = () => {
  return (
    <div className="welcome">
      <img src={logo} alt="welcome-logo" className="welcome-logo" />
      <Link to="/main" className="welcome-btn">
        나만의 작물 키우러 가기
      </Link>
    </div>
  );
};

export default Welcome;
