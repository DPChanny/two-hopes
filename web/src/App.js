import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Main from "./pages/Main";
import Welcome from "./pages/Welcome";
import GroupDetail from "./pages/GroupDetail";
import CropDetail from "./pages/CropDetail";
import Scheduler from "./components/Scheduler";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/main" element={<Main />} />
          <Route path="/group/:id" element={<GroupDetail />} />
          <Route path="/crop/:id" element={<CropDetail />} />
          <Route path="/crop/:id/schedular" element={<Scheduler />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
