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

  /*useEffect(() => {
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

    fetchGroups();
  }, [searchQuery]);

  if (loading) return <p>로딩 중...</p>;*/

  // ✅ [🔧 수정 1] fetchGroups를 외부에서도 호출 가능하게 함수로 분리
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

  // ✅ [🔧 수정 2] useEffect에서 위 함수를 사용
  useEffect(() => {
    fetchGroups(); // ✅ 함수 호출
  }, [searchQuery]);

  if (loading) return <p>로딩 중...</p>;

  return (
    <div className="main">
      <Header />
      <SearchBar
        value={searchQuery}
        onChange={setSearchQuery}
        onSearch={() => {
          setLoading(true); // 검색 시 데이터 리로딩 유도
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
