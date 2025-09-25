import React, { useEffect, useState } from "react";

function DatasetViewer({ year }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/datasets/${year}`)
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch(() => setData({ error: "Failed to fetch data" }));
  }, [year]);

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Dataset for {year}</h2>
      <pre style={{ background: "#f4f4f4", padding: "10px" }}>
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}

export default DatasetViewer;
