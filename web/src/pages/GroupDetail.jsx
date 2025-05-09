import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BiMap } from "react-icons/bi";
import api from "../axiosConfig.js";
import { LuLeaf } from "react-icons/lu";
import "../styles/GroupDetail.css";
import AddBtn from "../components/AddBtn";

const GroupDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const groupId = parseInt(id);

  const [groupName, setGroupName] = useState("");
  const [location, setLocation] = useState("");
  const [crops, setCrops] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchGroup = async () => {
      try {
        const groupList = await api.get("/api/group/");
        const group = groupList.data.data.find((g) => g.group_id === groupId);

        if (!group) {
          setError("존재하지 않는 모임입니다.");
          return;
        }

        setGroupName(group.name);
        setLocation(group.location);
      } catch (err) {
        setError("그룹 정보를 불러오지 못했습니다.");
        console.error(err);
      }
    };

    const fetchCrops = async () => {
      try {
        const res = await api.get("/api/crop/", {
          params: { group_id: groupId },
        });
        setCrops(res.data.data);
      } catch (err) {
        console.error("작물 정보를 불러오지 못했습니다.", err);
      }
    };

    fetchGroup();
    fetchCrops();
  }, [groupId]);

  if (error) {
    return (
      <div>
        <h2>존재하지 않는 모임입니다.</h2>
        <h2>{error}</h2>
        <button onClick={() => navigate("/main")}>돌아가기</button>
      </div>
    );
  }

  return (
    <div className="group-detail">
      <h2>{groupName}</h2>
      <div className="group-detail-location">
        <BiMap size={35} />
        <p>{location}</p>
      </div>
      <div className="crop-container">
              {crops.map((crop) => (
        <div
          key={crop.id}
          className="crop-card"
          onClick={() => navigate(`/crop/${crop.crop_id}`)}
        >
          <div className="crop-title">
              <LuLeaf size={35} />
              <p>{crop.name}</p>
            </div>
            <div className="crop-status">{crop.harvest ? "수확 완료" : "미수확"}</div>
          </div>
        ))}
      </div>
      <AddBtn />
    </div>
  );
};

export default GroupDetail;
