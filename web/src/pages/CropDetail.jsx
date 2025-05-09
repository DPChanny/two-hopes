import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BiMap } from "react-icons/bi";
import { FaUserCircle } from "react-icons/fa";
import Scheduler from "../components/Scheduler";
import StatusCard from "../components/StatusCard";
import api from "../axiosConfig.js";
import "../styles/CropDetail.css";
import AddBtn from "../components/AddBtn";
import AddFormModal from "../components/AddFormModal.jsx";
import CommentSection from "../components/CommentSection";
import { TfiWrite } from "react-icons/tfi";
import PostSection from "../components/PostSection"; // ✅ [추가] 포스트 관련 UI 컴포넌트

const CropDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const cropId = parseInt(id);
  const [crop, setCrop] = useState(null);
  const [error, setError] = useState("");
  const [groupLocation, setGroupLocation] = useState("");
  const [groupName, setGroupName] = useState("");
  const [sensors, setSensors] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showPostModal, setShowPostModal] = useState(false); // ✅ [추가] 게시글 작성 모달

  const unitMap = {
    temperature: "°C",
    humidity: "%RH",
    light: "Lux",
    water: "",
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
          setGroupName(matchedGroup.name);
        } else {
          setGroupLocation("위치 정보 없음");
          setGroupName("그룹 정보 없음");
        }
      } catch (err) {
        console.error("작물 또는 그룹 정보 조회 실패:", err);
        setError("존재하지 않는 페이지입니다.");
      }
    };

    fetchCropAndGroup();
  }, [id]);
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
  useEffect(() => {
    fetchSensors();
    const interval = setInterval(fetchSensors, 1000);
    return () => clearInterval(interval);
  }, [id]);

  // ✅ [추가] 새 게시글을 crop state에 반영
  const handleNewPost = (newPost) => {
    setCrop((prev) => ({
      ...prev,
      posts: [newPost, ...prev.posts],
    }));
  };

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
      <div className="crop-detail-header">
        <h2>{groupName}</h2>
        <div className="crop-detail-location">
          <BiMap size={20} />
          <p>{groupLocation}</p>
        </div>
      </div>
      <div className="crop-detail-divider"></div>
      <div className="crop-detail-title">
        <h2>{name}</h2>
        <div className="crop-detail-title-p">
          <p>{harvest ? "수확 완료" : "미수확"}</p>
          <PostSection
            posts={posts}
            cropId={cropId}
            onPostAdded={handleNewPost}
            className="crop-detail-post-add"
          />
        </div>
      </div>
      <div className="crop-detail-content">
        <div className="crop-status-section">
          {sensors.map((sensor) => (
            <StatusCard
              key={sensor.sensor_id}
              label={sensor.name}
              value={`${sensor.value}${unitMap[sensor.sensor_type] || ""}`}
            />
          ))}
          <AddBtn onClick={() => setShowAddModal(true)} />
          {showAddModal && (
            <AddFormModal
              type="sensor"
              cropId={cropId}
              onSensorAdded={fetchSensors}
              onClose={() => setShowAddModal(false)}
            />
          )}
        </div>

        <div className="crop-posts-section">
          <div className="crop-posts">
            {posts.map((post) => (
              <div key={post.post_id} className="crop-post-card">
                <div className="crop-post-author">
                  <FaUserCircle size={36} />
                  <p>{post.author || "익명"}</p>
                </div>
                <img
                  src={post.image_url}
                  alt="작물 이미지"
                  className="crop-post-img"
                />
                <p>{post.content}</p>
                <div className="crop-post-bottom">
                  <CommentSection postId={post.post_id} />
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="crop-reserve-section">
          <Scheduler schedules={schedules} />
        </div>
      </div>
    </div>
  );
};

export default CropDetail;
