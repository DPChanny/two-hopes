import React, { useState } from "react";
import AddForm from "./AddForm";
import CustomSelect from "./CustomSelect";
import { RiCloseFill } from "react-icons/ri";
import "../styles/AddFormModal.css";
import api from "../axiosConfig";
import SensorSelect from "./SensorSelect";

const AddFormModal = ({
  type,
  onClose,
  onGroupAdded,
  onCropAdded,
  onSensorAdded,
  groupId,
  cropId, // 센서 추가에 필요
}) => {
  const [groupName, setGroupName] = useState("");
  const [location, setLocation] = useState("");
  const [cropName, setCropName] = useState("");
  const [cropType, setCropType] = useState(null);
  const [sensorName, setSensorName] = useState("");
  const [sensorType, setSensorType] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (type === "group") {
        const payload = {
          name: groupName,
          location: location,
        };
        const res = await api.post("/api/group/", payload);
        console.log("✅ 그룹 추가 응답:", res.data);
        if (onGroupAdded) onGroupAdded();
        onClose();
      } else if (type === "crop") {
        const payload = {
          group_id: groupId,
          name: cropName,
          crop_type: cropType?.value,
        };
        const res = await api.post("/api/crop/", payload);
        console.log("🌱 작물 추가 성공:", res.data);
        if (onCropAdded) onCropAdded();
        onClose();
      } else if (type === "sensor") {
        const payload = {
          crop_id: cropId,
          name: sensorName,
          sensor_type: sensorType?.value,
        };
        const res = await api.post("/api/sensor/", payload);
        console.log("📡 센서 추가 성공:", res.data);
        if (onSensorAdded) onSensorAdded();
        onClose();
      }
    } catch (error) {
      console.error("추가 실패:", error);
      alert("추가에 실패했습니다.");
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <RiCloseFill className="modal-close" onClick={onClose} size={36} />
        <AddForm
          title={
            type === "group"
              ? "그룹 추가"
              : type === "crop"
              ? "작물 추가"
              : "센서 추가"
          }
          onSubmit={handleSubmit}
        >
          {type === "group" ? (
            <div className="form-content-frame">
              <label className="form-label">‣ 그룹 이름</label>
              <input
                type="text"
                placeholder="그룹 이름"
                value={groupName}
                onChange={(e) => setGroupName(e.target.value)}
                className="form-input"
              />
              <label className="form-label">‣ 위치</label>
              <input
                type="text"
                placeholder="위치"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="form-input"
              />
            </div>
          ) : type === "crop" ? (
            <div className="form-content-frame">
              <label className="form-label">‣ 작물 이름</label>
              <input
                type="text"
                placeholder="작물 이름"
                value={cropName}
                onChange={(e) => setCropName(e.target.value)}
                className="form-input"
              />
              <label className="form-label">‣ 작물 종류</label>
              <CustomSelect
                className="form-select"
                placeholder="작물 종류"
                value={cropType}
                onChange={(selectedOption) => setCropType(selectedOption)}
              />
            </div>
          ) : (
            <div className="form-content-frame">
              <label className="form-label">‣ 센서 이름</label>
              <input
                type="text"
                placeholder="센서 이름"
                value={sensorName}
                onChange={(e) => setSensorName(e.target.value)}
                className="form-input"
              />
              <label className="form-label">‣ 센서 타입</label>
              <SensorSelect
                className="form-select"
                placeholder="센서 타입"
                value={sensorType}
                onChange={(selectedOption) => setSensorType(selectedOption)}
              />
            </div>
          )}
        </AddForm>
      </div>
    </div>
  );
};

export default AddFormModal;
