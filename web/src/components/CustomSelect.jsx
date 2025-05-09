import React from "react";
import Select from "react-select";

const CustomSelect = ({ className, placeholder, value, onChange }) => {
  const options = [
    { value: "vegetable", label: "야채" },
    { value: "fruit", label: "과일" },
    { value: "grain", label: "곡물" },
    { value: "root", label: "근채" },
  ];

  // 드롭다운 스타일
  const CustomStyle = {
    control: (base) => ({
      ...base,
      backgroundColor: "#fff",
      width: "128px",
      height: "48px",
      border: "none",
      borderRadius: "20px",
      paddingRight: "8px",
      boxSizing: "border-box",
    }),
    placeholder: (base) => ({
      ...base,
      color: "black",
      fontFamily: "Pretendard",
      fontSize: "20px",
      margin: "0px",
      padding: "0px",
      lineHeight: "48px",
      width: "100%",
      textAlign: "right",
    }),
    singleValue: (base) => ({
      ...base,
      color: "black",
      fontSize: "20px",
      margin: "0px",
      padding: "0px",
      lineHeight: "48px",
      width: "100%",
      textAlign: "right",
    }),
    input: (base) => ({
      ...base,
      margin: "0px",
      padding: "0px",
      height: "1px",
      width: "1px",
      minWidth: "0px",
      overflow: "hidden",
    }),
    valueContainer: (base) => ({
      ...base,
      padding: "0px",
      display: "flex",
      alignItems: "center",
    }),
    indicatorSeparator: () => ({
      display: "none",
    }),
    menu: (base) => ({
      ...base,
      marginTop: "-10px",
      fontSize: "20px",
    }),
  };

  return (
    <Select
      className={className}
      placeholder={placeholder}
      options={options}
      styles={CustomStyle}
      value={value}
      onChange={onChange}
    />
  );
};

export default CustomSelect;
