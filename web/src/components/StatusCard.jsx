import React from "react";

const StatusCard = ({ label, value }) => {
  return (
    <div className="status-card">
      <span>{label}</span>
      <span>{value}</span>
    </div>
  );
};

export default StatusCard;
