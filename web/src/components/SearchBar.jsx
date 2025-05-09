import React from "react";
import { RiSearchLine } from "react-icons/ri";
import "../styles/SearchBar.css";

const SearchBar = ({ value, onChange, onSearch }) => {
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      onSearch(); // 부모에게 검색 요청
    }
  };

  return (
    <div className="searchbar">
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="검색어를 입력하세요"
      />
      <RiSearchLine className="search-button" size={24} onClick={onSearch} />
    </div>
  );
};

export default SearchBar;
