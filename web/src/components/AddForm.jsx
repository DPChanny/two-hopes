import React from "react";

const AddForm = ({ title, onSubmit, children, buttonLabel }) => {
  return (
    <form className="add-form" onSubmit={onSubmit}>
      <div className="add-form-title">{title}</div>
      <div className="add-form-input">{children}</div>
      <button type="submit" label={buttonLabel} />
    </form>
  );
};

export default AddForm;
