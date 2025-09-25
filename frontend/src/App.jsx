import React, { useState } from "react";
import DatasetViewer from "./components/DatasetViewer";

function App() {
  const [year, setYear] = useState("");
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>INGRES Chatbot Data Viewer</h1>
      <input
        type="text"
        placeholder="Enter year (e.g., 2021)"
        value={year}
        onChange={(e) => setYear(e.target.value)}
      />
      {year && <DatasetViewer year={year} />}
    </div>
  );
}

export default App;
