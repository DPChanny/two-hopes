import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { groups, cropPosts } from "../data/dummyData";
import { BiMap } from "react-icons/bi";
import { BsHeart, BsHeartFill } from "react-icons/bs";

const CropDetail = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const cropId = parseInt(id);
  const posts = cropPosts.filter((post) => post.cropId === cropId);

  let matchedGroup = null;
  let matchedCrop = null;

  for (const group of groups) {
    const crop = group.crops?.find((c) => c.id === cropId);
    if (crop) {
      matchedGroup = group;
      matchedCrop = crop;
      break;
    }
  }

  if (!matchedCrop || !matchedGroup) {
    return (
      <div>
        <h2>존재하지 않는 페이지입니다.</h2>
        <button onClick={() => navigate("/main")}>돌아가기</button>
      </div>
    );
  }

  return (
    <div className="crop-detail">
      <div className="crop-detail-group">
        <p>{matchedGroup.title}</p>
        <BiMap />
        <p>{matchedGroup.location}</p>
      </div>
      <hr />
      <div className="crop-detail-title">
        <h2>{matchedCrop.name}</h2>
        <p>{matchedCrop.status}</p>
      </div>
      <div className="crop-posts">
        {posts.map((post) => (
          <div key={post.id} className="crop-post-card">
            <img src={post.postImg} />
            <p>{post.content}</p>
            {post.liked ? <BsHeart /> : <BsHeartFill />}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CropDetail;
