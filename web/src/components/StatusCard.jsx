import React from "react";
import "../styles/StatusCard.css";

const StatusCard = ({ label, value }) => {
  return (
    <div className="status-card">
      <h3>{label}</h3>
      <p>{value}</p>
    </div>
  );
};

export default StatusCard;
