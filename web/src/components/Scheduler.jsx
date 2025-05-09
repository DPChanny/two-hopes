import React, { useState } from "react";
import { groups } from "../data/dummyData";
import { useNavigate, useParams } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Scheduler = () => {
  const { id } = useParams();
  const cropId = parseInt(id);
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedTime, setSelectedTime] = useState(null);

  const reservedSlots = {
    "2023-05-28": ["09:00", "10:00", "16:00"],
    "2023-05-29": ["13:00"],
  };

  const timeOptions = [
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
  ];

  let matchedCropName = null;

  for (const group of groups) {
    const crop = group.crops?.find((c) => c.id === cropId);
    if (crop) {
      matchedCropName = crop.name;
      break;
    }
  }

  if (!matchedCropName) {
    return (
      <div>
        <h2>존재하지 않는 페이지입니다.</h2>
        <button onClick={() => navigate("/main")}>돌아가기</button>
      </div>
    );
  }

  const handleChange = (newSchedule) => {
    setSchedule(newSchedule);
  };

  return (
    <div className="schedular">
      <h1>{matchedCropName}</h1>
      날짜 선택
      <DatePicker
        selected={selectedDate}
        onChange={(date) => {
          setSelectedDate(date);
          setSchedule([]);
        }}
        dateFormat="yyyy-MM-dd"
        minDate={new Date()}
      />
    </div>
  );
};

export default Scheduler;
