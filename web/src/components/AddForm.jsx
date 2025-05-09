import React from "react";
import "../styles/AddForm.css";

const AddForm = ({ onSubmit, children, buttonLabel }) => {
  return (
    <form className="add-form" onSubmit={onSubmit}>
      <div className="add-form-input">{children}</div>
      <button type="submit" className="add-form-btn">
        추가
      </button>
    </form>
  );
};

export default AddForm;
