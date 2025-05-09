import React from "react";
import Select from "react-select";

const SensorSelect = ({ className, placeholder, value, onChange }) => {
  const options = [
    { value: "temperature", label: "온도" },
    { value: "humidity", label: "습도" },
    { value: "light", label: "조도" },
    { value: "water", label: "수분" },
  ];

  const customStyle = {
    control: (base) => ({
      ...base,
      backgroundColor: "#fff",
      width: "396px",
      height: "48px",
      border: "1px solid #ccc",
      borderRadius: "10px",
      paddingLeft: "10px",
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
    }),
    singleValue: (base) => ({
      ...base,
      color: "black",
      fontSize: "20px",
      margin: "0px",
      padding: "0px",
      lineHeight: "48px",
      width: "100%",
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
      styles={customStyle}
      value={value}
      onChange={onChange}
    />
  );
};

export default SensorSelect;
