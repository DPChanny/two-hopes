import React, { useState } from "react";
import { groups } from "../data/dummyData";
import { useNavigate, useParams } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../styles/Scheduler.css";

const Scheduler = () => {
  const { id } = useParams();
  const cropId = parseInt(id);
  const navigate = useNavigate();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedTimes, setSelectedTimes] = useState([]);

  const reservedSlots = {
    "2025-05-09": ["09:00", "10:00", "16:00"],
    "2023-05-10": ["13:00"],
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

  const formatDate = (date) => date.toISOString().slice(0, 10);

  const handleTimeSelect = (time) => {
    const isSelected = selectedTimes.includes(time);

    if (isSelected) {
      setSelectedTimes(selectedTimes.filter((t) => t !== time));
    } else {
      if (selectedTimes.length >= 3) return;
      setSelectedTimes([...selectedTimes, time]);
    }
  };

  const isReserved = (date, time) => {
    const dateKey = formatDate(date);
    return reservedSlots[dateKey]?.includes(time);
  };

  return (
    <div className="schedular">
      날짜 선택
      <DatePicker
        selected={selectedDate}
        onChange={(date) => {
          setSelectedDate(date);
          setSelectedTimes(null);
        }}
        dateFormat="yyyy-MM-dd"
        minDate={new Date()}
      />
      <div className="time-selector">
        <label>예약 시간</label>
        <p>3시간까지 선택 가능합니다.</p>
        <div className="time-grid">
          {timeOptions.map((time) => {
            const disabled = isReserved(selectedDate, time);
            const isSelected = selectedTimes.includes(time);

            return (
              <button
                key={time}
                className={`time-btn ${disabled ? "disabled" : ""} ${
                  isSelected ? "selected" : ""
                }`}
                onClick={() => !disabled && handleTimeSelect(time)}
              >
                {time} ~ {String(+time.slice(0, 2) + 1).padStart(2, "0")}:00
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Scheduler;
