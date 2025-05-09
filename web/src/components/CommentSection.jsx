import React, { useEffect, useState } from "react";
import api from "../axiosConfig";
import { FaRegCommentAlt } from "react-icons/fa";
import "../styles/CommentSection.css";

const CommentSection = ({ postId }) => {
  const [comments, setComments] = useState([]);
  const [showComments, setShowComments] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [authorName, setAuthorName] = useState(""); // 🆕

  useEffect(() => {
    api
      .get("/api/comment/", { params: { post_id: postId } })
      .then((res) => setComments(res.data.data))
      .catch((err) => console.error("댓글 불러오기 실패:", err));
  }, [postId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    try {
      const res = await api.post("/api/comment/", {
        post_id: postId,
        content: newComment,
        author: authorName.trim() || "익명", // 🆕
      });
      setComments((prev) => [...prev, res.data.data]);
      setNewComment("");
      setAuthorName(""); // 🆕 작성 후 초기화
    } catch (err) {
      console.error("댓글 추가 실패:", err);
    }
  };

  return (
    <div className="commnet-section">
      <div
        onClick={() => setShowComments((prev) => !prev)}
        style={{ cursor: "pointer" }}
        className="comment-icon"
      >
        <FaRegCommentAlt size={35} />
      </div>

      {showComments && (
        <div className="comment-content">
          <form onSubmit={handleSubmit} className="comment-input">
            <input
              type="text"
              placeholder="작성자 이름"
              value={authorName}
              onChange={(e) => setAuthorName(e.target.value)}
            />
            <input
              type="text"
              placeholder="댓글 입력"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
            />
            <button type="submit">작성</button>
          </form>
          <div className="comments-list">
            {comments.length > 0 ? (
              comments.map((c, index) => (
                <div key={c.comment_id} className="comments-list-item">
                  <b>{c.author}</b>
                  <div className="vertical-line" />
                  <span>{c.content}</span>
                </div>
              ))
            ) : (
              <p>댓글이 없습니다.</p>
            )}
          </div>
        </div>
      )}

      {!showComments && comments.length > 0 && (
        <div className="comment-preview">
          <b>{comments[0].author}</b>: {comments[0].content}
        </div>
      )}
    </div>
  );
};

export default CommentSection;
