import React from "react";
import { BiPlus } from "react-icons/bi";
import "../styles/AddBtn.css";

const AddBtn = () => {
  return (
    <div className="add-btn">
      <BiPlus size={30} />
    </div>
  );
};

export default AddBtn;
