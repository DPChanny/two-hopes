import React from "react";
import "../styles/Main.css";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import { groups } from "../data/dummyData";
import { BiMap } from "react-icons/bi";
import { useNavigate } from "react-router-dom";

const Main = () => {
  const navigate = useNavigate();

  return (
    <div className="main">
      <Header />
      <SearchBar />
      {groups.map((group) => (
        <div
          key={group.id}
          className="group-card"
          onClick={() => navigate(`/group/${group.id}`)}
        >
          <h2>{group.title}</h2>
          <div className="group-location">
            <BiMap />
            <p>{group.location}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Main;
