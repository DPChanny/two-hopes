import React from "react";
import { BiPlus } from "react-icons/bi";
import "../styles/AddBtn.css";
import { useNavigate } from "react-router-dom";

const AddBtn = ({ type, onClick }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    if (onClick) {
      onClick();
    } else if (type) {
      navigate(`/add/${type}`);
    }
  };

  return (
    <div className="add-btn" onClick={handleClick}>
      <BiPlus size={30} />
    </div>
  );
};

export default AddBtn;
