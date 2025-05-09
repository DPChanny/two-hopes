// components/PostSection.jsx
import React, { useState } from "react";
import { IoMdDocument } from "react-icons/io";
import AddFormModal from "./AddFormModal";

const PostSection = ({ posts, cropId, onPostAdded }) => {
  const [showForm, setShowForm] = useState(false);

  const handlePostAdded = (newPost) => {
    if (onPostAdded) onPostAdded(newPost);
    setShowForm(false); // ✅ 작성 후 폼 닫기
  };

  return (
    <div className="crop-posts-sec">
      <div className="post-section-header">
        <IoMdDocument
          size={30}
          className="write-icon"
          onClick={() => setShowForm((prev) => !prev)}
          style={{ cursor: "pointer" }}
        />
      </div>

      {showForm && (
        <AddFormModal
          type="post"
          cropId={cropId}
          onPostAdded={handlePostAdded}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
};

export default PostSection;
