import axios from "axios";

const api = axios.create({
  baseURL: "http://3.26.202.82:8000",
  withCredentials: false,
});

export default api;
