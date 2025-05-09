import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BiMap } from "react-icons/bi";
//import { BsHeart, BsHeartFill } from "react-icons/bs";
import Scheduler from "../components/Scheduler";
import StatusCard from "../components/StatusCard";
import api from "../axiosConfig.js";
import "../styles/CropDetail.css";
import AddBtn from "../components/AddBtn";
import AddFormModal from "../components/AddFormModal.jsx";
//import { GoCommentDiscussion } from "react-icons/go";
import CommentSection from "../components/CommentSection"; // ✅ 추가

const CropDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [crop, setCrop] = useState(null);
  const [error, setError] = useState("");
  const [groupLocation, setGroupLocation] = useState("");
  const [sensors, setSensors] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);

  const unitMap = {
    temperature: "°C",
    humidity: "%RH",
    light: "Lux",
    water: "%",
  };

  useEffect(() => {
    const fetchCropAndGroup = async () => {
      try {
        const res = await api.get(`/api/crop/${id}`);
        const cropData = res.data.data;
        setCrop(cropData);

        const groupRes = await api.get("/api/group/");
        const matchedGroup = groupRes.data.data.find(
          (group) => group.group_id === cropData.group_id
        );

        if (matchedGroup) {
          setGroupLocation(matchedGroup.location);
        } else {
          setGroupLocation("위치 정보 없음");
        }
      } catch (err) {
        console.error("작물 또는 그룹 정보 조회 실패:", err);
        setError("존재하지 않는 페이지입니다.");
      }
    };

    fetchCropAndGroup();
  }, [id]);

  useEffect(() => {
    const fetchSensors = async () => {
      try {
        const res = await api.get("/api/sensor/", {
          params: { crop_id: id },
        });
        setSensors(res.data.data);
      } catch (err) {
        console.error("센서 정보 조회 실패:", err);
      }
    };

    fetchSensors();
    const interval = setInterval(fetchSensors, 1000);
    return () => clearInterval(interval);
  }, [id]);

  if (error) {
    return (
      <div>
        <h2>{error}</h2>
        <button onClick={() => navigate("/main")}>돌아가기</button>
      </div>
    );
  }

  if (!crop) return <p>로딩 중...</p>;

  const { name, harvest, posts, schedules } = crop;

  return (
    <div className="crop-detail">
      <div className="crop-detail-group">
        <p>작물유형: {name}</p>
        <BiMap />
        <p>위치 : {groupLocation}</p>
      </div>
      <hr />
      <div className="crop-detail-title">
        <h2>{name}</h2>
        <p>{harvest ? "수확 필요" : "성장중"}</p>
      </div>
      <div className="crop-status-section">
        {sensors.map((sensor) => (
          <StatusCard
            key={sensor.sensor_id}
            label={sensor.name}
            value={`${sensor.value} ${unitMap[sensor.sensor_type] || ""}`}
          />
        ))}
      </div>
      <AddBtn onClick={() => setShowAddModal(true)} />
      {showAddModal && (
        <AddFormModal type="sensor" onClose={() => setShowAddModal(false)} />
      )}
      <div className="crop-posts-section">
        {posts.map((post) => (
          <div key={post.post_id} className="crop-post-card">
            <p>👤 {post.author || "익명"}</p>
            <img
              src={post.image_url}
              alt="작물 이미지"
              style={{
                width: "100%",
                maxWidth: "300px",
                height: "auto",
                borderRadius: "10px",
              }}
            />
            <p>{post.content}</p>
            console.log("CommentSection:", CommentSection);
            <CommentSection postId={post.post_id} />
          </div>
        ))}
      </div>
      <div className="crop-reserve-section">
        <Scheduler schedules={schedules} />
      </div>
    </div>
  );
};

export default CropDetail;
