import React, { useState } from "react";
import AddForm from "./AddForm";
import CustomSelect from "./CustomSelect";
import { RiCloseFill } from "react-icons/ri";
import "../styles/AddFormModal.css";

const AddFormModal = ({ type, onClose }) => {
  const [groupName, setGroupName] = useState("");
  const [location, setLocation] = useState("");
  const [cropName, setCropName] = useState("");
  const [cropType, setCropType] = useState(null);

  const handleSubmit = (e) => {
    //api 처리
    if (type === "group") {
    } else if (type === "crop") {
    }
    onClose();
  };
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <RiCloseFill className="modal-close" onClick={onClose} size={36} />
        <AddForm
          title={type === "group" ? "그룹 추가" : "작물 추가"}
          onSubmit={handleSubmit}
          buttonLabel="추가"
        >
          {type === "group" ? (
            <>
              <input
                type="text"
                placeholder="그룹 이름"
                value={groupName}
                onChange={(e) => setGroupName(e.target.value)}
              />
              <input
                type="text"
                placeholder="위치"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </>
          ) : (
            <>
              <input
                type="text"
                placeholder="작물 이름"
                value={cropName}
                onChange={(e) => setCropName(e.target.value)}
              />
              <CustomSelect
                className="crop-type-select"
                placeholder="작물 종류"
                value={cropType}
                onChange={(selectedOption) => setCropType(selectedOption)}
              />
            </>
          )}
        </AddForm>
      </div>
    </div>
  );
};

export default AddFormModal;
