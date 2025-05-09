import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BiMap } from "react-icons/bi";
import { BsHeart, BsHeartFill } from "react-icons/bs";
import { FaUserCircle } from "react-icons/fa";
import Scheduler from "../components/Scheduler";
import StatusCard from "../components/StatusCard";
import api from "../axiosConfig.js";
import "../styles/CropDetail.css";

const CropDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [crop, setCrop] = useState(null);
  const [error, setError] = useState("");
  const [groupLocation, setGroupLocation] = useState("");
  const [groupName, setGroupName] = useState("");
  const [sensors, setSensors] = useState([]);
  const statusItems = [
    { label: "온도", type: "temperature" },
    { label: "습도", type: "humidity" },
    { label: "일조량", type: "light" },
  ];

  useEffect(() => {
    const fetchCropAndGroup = async () => {
      try {
        const res = await api.get(`/api/crop/${id}`);
        const cropData = res.data.data;
        setCrop(cropData);

        // 그룹 정보 요청
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

    fetchSensors(); // 최초 1회 실행

    const interval = setInterval(fetchSensors, 1000); // 10초마다 호출
    return () => clearInterval(interval); // 언마운트 시 정리
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

  const getSensorValue = (type) => {
    const sensor = sensors.find((s) => s.sensor_type === type);
    return sensor ? sensor.value : "정보 없음";
  };

  return (
    <div className="crop-detail">
      <div className="crop-detail-header">
        <h2>{groupName}</h2>
        <div className="crop-detail-location">
          <BiMap size={35} />
          <p>{groupLocation}</p>
        </div>
      </div>
      <div className="crop-detail-content">
        <div className="crop-status-section">
          {statusItems.map((item) => (
            <StatusCard
              key={item.type}
              label={item.label}
              value={getSensorValue(item.type)}
            />
          ))}
        </div>
        <div className="crop-posts-section">
          <div className="crop-detail-title">
            <h2>{name}</h2>
            <p>{harvest ? "수확 완료" : "미수확"}</p>
          </div>
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
                  <BsHeart size={32} className="crop-post-icon" />
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="crop-reserve-section">
          예약하기
          <Scheduler schedules={schedules} />
        </div>
      </div>
    </div>
  );
};

export default CropDetail;
