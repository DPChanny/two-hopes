// Scheduler.jsx
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../axiosConfig";
import "../styles/Scheduler.css";

const WEEKDAYS = ["월", "화", "수", "목", "금", "토", "일"];
const START_HOUR = 0;
const END_HOUR = 24;
const TIMELINE_HEIGHT = 600;
const PIXEL_PER_MINUTE = TIMELINE_HEIGHT / ((END_HOUR - START_HOUR) * 60);
const WEEKDAY_STR_TO_INDEX = {
  Mon: 0,
  Tue: 1,
  Wed: 2,
  Thu: 3,
  Fri: 4,
  Sat: 5,
  Sun: 6,
};
const WEEKDAY_INDEX_TO_STR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function timeToMinutes(t) {
  const [h, m] = t.split(":").map(Number);
  return h * 60 + m;
}

function toTimeString(m) {
  return `${String(Math.floor(m / 60)).padStart(2, "0")}:${String(
    m % 60
  ).padStart(2, "0")}`;
}

function generateTimeLabels() {
  const times = [];
  for (let h = START_HOUR; h <= END_HOUR; h++) {
    times.push(`${String(h).padStart(2, "0")}:00`);
  }
  return times;
}

function isOverlap(target, others) {
  const s1 = timeToMinutes(target.start_time);
  const e1 = timeToMinutes(target.end_time);
  return others.some((s) => {
    if (s.schedule_id === target.schedule_id) return false;
    if (s.weekday !== target.weekday) return false;
    const s2 = timeToMinutes(s.start_time);
    const e2 = timeToMinutes(s.end_time);
    return s1 < e2 && e1 > s2;
  });
}

export default function Scheduler() {
  const [schedules, setSchedules] = useState([]);
  const [dragInfo, setDragInfo] = useState(null);
  const [drawInfo, setDrawInfo] = useState(null);
  const [, setModified] = useState(null);
  const { id } = useParams();
  const cropId = parseInt(id);

  useEffect(() => {
    axios.get(`/api/schedule/?crop_id=${cropId}`).then((res) => {
      const data = res.data.data ?? [];
      setSchedules(
        data.map((s) => ({ ...s, weekday: WEEKDAY_STR_TO_INDEX[s.weekday] }))
      );
    });
  }, [cropId]);

  const handleMouseDown = (e, s, type) => {
    e.stopPropagation();
    setDragInfo({
      type,
      schedule: s,
      startY: e.clientY,
      startX: e.clientX,
      originalTop: timeToMinutes(s.start_time),
      originalBottom: timeToMinutes(s.end_time),
      originalWeekday: s.weekday,
    });
  };

  const handleMouseMove = (e) => {
    if (dragInfo) {
      const deltaMin = Math.round(
        (e.clientY - dragInfo.startY) / PIXEL_PER_MINUTE
      );
      const dayDelta = Math.floor((e.clientX - dragInfo.startX) / 120);

      setSchedules((prev) =>
        prev.map((s) => {
          if (s.schedule_id !== dragInfo.schedule.schedule_id) return s;
          let start = dragInfo.originalTop;
          let end = dragInfo.originalBottom;
          let weekday = dragInfo.originalWeekday + dayDelta;
          if (dragInfo.type === "move") {
            start += deltaMin;
            end += deltaMin;
          } else if (dragInfo.type === "resize") {
            end += deltaMin;
          }
          if (end <= start) end = start + 1;
          const updated = {
            ...s,
            start_time: toTimeString(Math.max(start, 0)),
            end_time: toTimeString(Math.min(end, 1440)),
            weekday: Math.max(0, Math.min(6, weekday)),
          };
          setModified(updated);
          return updated;
        })
      );
    } else if (drawInfo) {
      const bounds = document
        .querySelector(`.day-column[data-day='${drawInfo.dayIndex}']`)
        .getBoundingClientRect();
      const offsetY = e.clientY - bounds.top;
      setDrawInfo((prev) => ({ ...prev, currentY: offsetY }));
    }
  };

  const handleMouseUp = async (e) => {
    if (dragInfo) {
      const deltaMin = Math.round(
        (e.clientY - dragInfo.startY) / PIXEL_PER_MINUTE
      );
      const dayDelta = Math.floor((e.clientX - dragInfo.startX) / 120);

      const start =
        dragInfo.originalTop + (dragInfo.type === "move" ? deltaMin : 0);
      const end = dragInfo.originalBottom + deltaMin;
      const weekday = Math.max(
        0,
        Math.min(6, dragInfo.originalWeekday + dayDelta)
      );

      const updated = {
        ...dragInfo.schedule,
        start_time: toTimeString(Math.max(start, 0)),
        end_time: toTimeString(Math.min(end, 1440)),
        weekday,
      };

      if (isOverlap(updated, schedules)) {
        setSchedules((prev) =>
          prev.map((s) =>
            s.schedule_id === dragInfo.schedule.schedule_id
              ? {
                  ...s,
                  start_time: toTimeString(dragInfo.originalTop),
                  end_time: toTimeString(dragInfo.originalBottom),
                  weekday: dragInfo.originalWeekday,
                }
              : s
          )
        );
      } else {
        try {
          console.log("hi");
          await axios.patch(`/api/schedule/${updated.schedule_id}`, {
            weekday: WEEKDAY_INDEX_TO_STR[updated.weekday],
            start_time: updated.start_time,
            end_time: updated.end_time,
            author: updated.author,
          });
          setSchedules((prev) =>
            prev.map((s) =>
              s.schedule_id === updated.schedule_id ? updated : s
            )
          );
        } catch (err) {
          alert("수정 실패");
        }
      }
      setDragInfo(null);
    } else if (drawInfo) {
      const { startY, currentY, dayIndex } = drawInfo;
      const y1 = Math.min(startY, currentY);
      const y2 = Math.max(startY, currentY);
      const startMinutes = Math.round((y1 / TIMELINE_HEIGHT) * 1440);
      const endMinutes = Math.round((y2 / TIMELINE_HEIGHT) * 1440);
      const startTime = toTimeString(startMinutes);
      const endTime = toTimeString(endMinutes);
      const author = window.prompt(
        `새 스케줄 추가 (${WEEKDAYS[dayIndex]} ${startTime} ~ ${endTime})\n작성자 이름을 입력하세요:`
      );
      if (author && author.trim()) {
        try {
          const res = await axios.post("/api/schedule/", {
            crop_id: cropId,
            weekday: WEEKDAY_INDEX_TO_STR[dayIndex],
            start_time: startTime,
            end_time: endTime,
            author: author.trim(),
          });
          const newItem = res.data.data;
          setSchedules((prev) => [
            ...prev,
            { ...newItem, weekday: WEEKDAY_STR_TO_INDEX[newItem.weekday] },
          ]);
        } catch (err) {
          alert("추가 실패");
        }
      }
      setDrawInfo(null);
    }
  };

  const handleColumnDown = (e, dayIndex) => {
    const bounds = e.currentTarget.getBoundingClientRect();
    const offsetY = e.clientY - bounds.top;
    setDrawInfo({
      isDrawing: true,
      dayIndex,
      startY: offsetY,
      currentY: offsetY,
    });
  };

  const handleClick = async (s) => {
    if (!window.confirm("삭제하시겠습니까?")) return;
    try {
      await axios.delete(`/api/schedule/${s.schedule_id}`);
      setSchedules((prev) =>
        prev.filter((v) => v.schedule_id !== s.schedule_id)
      );
    } catch (err) {
      alert("삭제 실패");
    }
  };

  const timeLabels = generateTimeLabels();

  return (
    <div
      className="scheduler"
      onMouseMove={handleMouseMove}
      onMouseUp={(e) => handleMouseUp(e)} // `e` 전달
    >
      <div className="time-column">
        {timeLabels.map((label) => (
          <div key={label} className="time-label">
            {label}
          </div>
        ))}
      </div>

      {WEEKDAYS.map((day, col) => (
        <div
          key={day}
          className="day-column"
          data-day={col}
          onMouseDown={(e) => handleColumnDown(e, col)} // `e` 전달
        >
          <div className="day-label">{day}</div>
          {timeLabels.map((_, idx) => (
            <div
              key={idx}
              className="hour-line"
              style={{ top: `${idx * 25}px` }}
            />
          ))}

          {drawInfo && drawInfo.dayIndex === col && (
            <div
              className="drag-preview"
              style={{
                top: `${Math.min(drawInfo.startY, drawInfo.currentY)}px`,
                height: `${Math.abs(drawInfo.startY - drawInfo.currentY)}px`,
              }}
            />
          )}

          {schedules
            .filter((s) => s.weekday === col)
            .map((s) => {
              const top = timeToMinutes(s.start_time) * PIXEL_PER_MINUTE;
              const height =
                (timeToMinutes(s.end_time) - timeToMinutes(s.start_time)) *
                PIXEL_PER_MINUTE;
              const conflict = isOverlap(s, schedules);
              return (
                <div
                  key={s.schedule_id}
                  className={`schedule-block${conflict ? " conflict" : ""}`}
                  style={{ top: `${top}px`, height: `${height}px` }}
                  onMouseDown={(e) => handleMouseDown(e, s, "move")} // `e` 전달
                  onDoubleClick={() => handleClick(s)}
                  title={`${s.author}: ${s.start_time}~${s.end_time}`}
                >
                  {s.author}
                  <div
                    className="resize-handle"
                    onMouseDown={(e) => handleMouseDown(e, s, "resize")} // `e` 전달
                  />
                </div>
              );
            })}
        </div>
      ))}
    </div>
  );
}
