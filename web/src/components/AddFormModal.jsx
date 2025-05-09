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
  onPostAdded, // ✅ [추가] 게시글 추가 콜백
  groupId,
  cropId, // 센서 추가에 필요
}) => {
  const [groupName, setGroupName] = useState("");
  const [location, setLocation] = useState("");
  const [cropName, setCropName] = useState("");
  const [cropType, setCropType] = useState(null);
  const [sensorName, setSensorName] = useState("");
  const [sensorType, setSensorType] = useState(null);
  const [postContent, setPostContent] = useState(""); // ✅ [추가] 게시글 내용
  const [imageUrl, setImageUrl] = useState(""); // ✅ [추가] 게시글 이미지 URL
  const [author, setAuthor] = useState("익명"); // ✅ 새로 추가

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
      } else if (type === "post") {
        const payload = {
          crop_id: cropId,
          content: postContent,
          author: author,
        };
        const res = await api.post("/api/post/", payload);
        await api.put(res.data.data.image_url, imageUrl, {
          headers: {
            "Content-Type": "image/jpeg",
          },
        });
        console.log(res.data.data.image_url);
        console.log(res.data.data.image_url.split("?"));
        const payload2 = {
          image_url: res.data.data.image_url.split("?")[0],
        };
        const res2 = await api.patch(
          `/api/post/${res.data.data.post_id}`,
          payload2
        );
        if (onPostAdded) onPostAdded(res2.data.data); // 부모에게 새 게시글 전달
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
              : type === "sensor"
              ? "센서 추가"
              : "게시글 작성" // ✅ [추가] post용 제목
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
          ) : type === "sensor" ? (
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
          ) : (
            <div className="form-content-frame">
              <input
                type="text"
                placeholder="작성자 이름"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                className="form-input"
              />
              <input
                type="file"
                accept=".jpg,image/jpeg"
                onChange={(e) => setImageUrl(e.target.files[0])}
                className="form-input"
              />
              <input
                type="text"
                placeholder="게시글 내용"
                value={postContent}
                onChange={(e) => setPostContent(e.target.value)}
                className="form-input"
              />
            </div>
          )}
        </AddForm>
      </div>
    </div>
  );
};

export default AddFormModal;
