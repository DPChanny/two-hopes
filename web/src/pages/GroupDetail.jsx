import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { groups } from "../data/dummyData";
import { BiMap } from "react-icons/bi";
import { LuLeaf } from "react-icons/lu";
import "../styles/GroupDetail.css";
import AddBtn from "../components/AddBtn";

const GroupDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const groupId = parseInt(id);
  const group = groups.find((g) => g.id === groupId);

  console.log("groupId:", groupId);
  console.log("group:", group);

  if (!group) {
    return (
      <div>
        <h2>존재하지 않는 모임입니다.</h2>
        <button onClick={() => navigate("/main")}>돌아가기</button>
      </div>
    );
  }

  return (
    <div className="group-detail">
      <h2>{group.title}</h2>
      <div className="group-detail-location">
        <BiMap size={35} />
        <p>{group.location}</p>
      </div>
      <div className="crop-container">
        {group.crops?.map((crop) => (
          <div
            key={crop.id}
            className="crop-card"
            onClick={() => navigate(`/crop/${crop.id}`)}
          >
            <div className="crop-title">
              <LuLeaf size={35} />
              <p>{crop.name}</p>
            </div>
            <div className="crop-status">{crop.status}</div>
          </div>
        ))}
      </div>
      <AddBtn />
    </div>
  );
};

export default GroupDetail;
