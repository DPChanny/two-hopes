import React, { useState } from "react";
import AddForm from "./AddForm";
import CustomSelect from "./CustomSelect";
import { RiCloseFill } from "react-icons/ri";
import "../styles/AddFormModal.css";
import api from "../axiosConfig";

const AddFormModal = ({
  type,
  onClose,
  onGroupAdded,
  groupId,
  onCropAdded,
}) => {
  const [groupName, setGroupName] = useState("");
  const [location, setLocation] = useState("");
  const [cropName, setCropName] = useState("");
  const [cropType, setCropType] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (type === "group") {
        const payload = {
          name: groupName,
          location: location,
        };

        const res = await api.post("/api/group/", payload);
        //const newGroup = res.data.data;
        console.log("✅ 그룹 추가 응답:", res.data); // ✅ 이제 문제 없음

        // 리스트에 추가 (Main에서 props로 콜백 전달 시)
        if (onGroupAdded) onGroupAdded();
        onClose();
      }

      // 나중에 crop 처리도 여기에 추가
      else if (type === "crop") {
        const payload = {
          group_id: groupId, // 이 props도 상단에서 받아야 함!
          name: cropName,
          crop_type: cropType?.value,
        };

        const res = await api.post("/api/crop/", payload);
        console.log("🌱 작물 추가 성공:", res.data);

        if (onCropAdded) onCropAdded(); // props로 콜백 전달하면 작물 목록 새로고침 가능
        onClose();
      }
    } catch (error) {
      console.error("그룹 추가 실패:", error);
      alert("그룹 추가에 실패했습니다.");
    }
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
