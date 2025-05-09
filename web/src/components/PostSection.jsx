// components/PostSection.jsx
import React, { useState } from "react";
import { TfiWrite } from "react-icons/tfi";
import AddFormModal from "./AddFormModal";

const PostSection = ({ posts, cropId, onPostAdded }) => {
  const [showForm, setShowForm] = useState(false);

  const handlePostAdded = (newPost) => {
    if (onPostAdded) onPostAdded(newPost);
    setShowForm(false); // ✅ 작성 후 폼 닫기
  };

  return (
    <div className="crop-posts-section">
      <div className="post-section-header">
        <TfiWrite
          size={24}
          className="write-icon"
          onClick={() => setShowForm((prev) => !prev)}
          style={{ cursor: "pointer" }}
        />
      </div>

      {showForm && (
        <AddFormModal cropId={cropId} onPostAdded={handlePostAdded} />
      )}
    </div>
  );
};

export default PostSection;
