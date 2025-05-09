import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { groups } from "../data/dummyData";
import { BiMap } from "react-icons/bi";

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
      <div className="group-location">
        <BiMap />
        <p>{group.location}</p>
      </div>
      {group.crops?.map((crop) => (
        <div
          key={crop.id}
          className="crop-card"
          onClick={() => navigate(`/crop/${crop.id}`)}
        >
          <p>{crop.name}</p>
          <p>{crop.status}</p>
        </div>
      ))}
    </div>
  );
};

export default GroupDetail;
