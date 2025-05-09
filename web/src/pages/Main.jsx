import React from "react";
import "../styles/Main.css";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import { groups } from "../data/dummyData";
import { BiMap } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import AddBtn from "../components/AddBtn";

const Main = () => {
  const navigate = useNavigate();

  return (
    <div className="main">
      <Header />
      <SearchBar />
      <div className="group-container">
        {groups.map((group) => (
          <div
            key={group.id}
            className="group-card"
            onClick={() => navigate(`/group/${group.id}`)}
          >
            <h1>{group.title}</h1>
            <div className="group-location">
              <BiMap size={35} />
              <p>{group.location}</p>
            </div>
          </div>
        ))}
      </div>
      <AddBtn />
    </div>
  );
};

export default Main;
