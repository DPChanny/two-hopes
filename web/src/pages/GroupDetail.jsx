import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
//import { groups } from "../data/dummyData";
import { BiMap } from "react-icons/bi";
import api from "../axiosConfig.js";

const GroupDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const groupId = parseInt(id);
  //const group = groups.find((g) => g.id === groupId);

  const [groupName, setGroupName] = useState("");
  const [location, setLocation] = useState("");
  const [crops, setCrops] = useState([]);
  const [error, setError] = useState("");

  //console.log("groupId:", groupId);
  //console.log("group:", group);

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
      <div className="group-location">
        <BiMap />
        <p>{location}</p>
      </div>
      {crops.map((crop) => (
        <div
          key={crop.id}
          className="crop-card"
          onClick={() => navigate(`/crop/${crop.crop_id}`)}
        >
          <p>{crop.name}</p>
          {/*<p>{crop.status}</p>*/}
          <p>{crop.harvest ? "수확 완료" : "미수확"}</p>
        </div>
      ))}
    </div>
  );
};

export default GroupDetail;
