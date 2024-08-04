import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import FileUpload from "./components/FileUpload";
import RecognizeFace from "./components/RecognizeFace";

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/">Upload Face</Link>
            </li>
            <li>
              <Link to="/recognize">Recognize Face</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<FileUpload />} />
          <Route path="/recognize" element={<RecognizeFace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
