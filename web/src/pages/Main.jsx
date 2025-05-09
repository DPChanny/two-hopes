import React, { useEffect, useState } from "react";
import "../styles/Main.css";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import { BiMap } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import api from "../axiosConfig.js";
import AddBtn from "../components/AddBtn";
import AddFormModal from "../components/AddFormModal.jsx";

const Main = () => {
  const navigate = useNavigate();
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [showAddModal, setShowAddModal] = useState(false);

  const fetchGroups = async () => {
    try {
      const res = await api.get("/api/group/", {
        params: searchQuery ? { name: searchQuery } : {},
      });
      setGroups(res.data.data);
    } catch (error) {
      console.error("그룹 목록 불러오기 실패:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGroups();
  }, [searchQuery]);

  if (loading) return <p>로딩 중...</p>;

  return (
    <div className="main">
      <Header />
      <SearchBar
        value={searchQuery}
        onChange={setSearchQuery}
        onSearch={() => {
          setLoading(true);
        }}
      />
      <div className="group-container">
        {groups.map((group) => (
          <div
            key={group.group_id}
            className="group-card"
            onClick={() => navigate(`/group/${group.group_id}`)}
          >
            <h2>{group.name}</h2>
            <div className="group-location">
              <BiMap size={35} />
              <p>{group.location}</p>
            </div>
          </div>
        ))}
      </div>
      <AddBtn onClick={() => setShowAddModal(true)} />
      {showAddModal && (
        <AddFormModal
          type="group"
          onClose={() => setShowAddModal(false)}
          onGroupAdded={fetchGroups}
        />
      )}
    </div>
  );
};

export default Main;
