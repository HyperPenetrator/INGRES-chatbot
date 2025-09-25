import React, { useEffect, useState } from "react";
import { fetchYears, fetchDatasetsByYear, previewDataset, downloadDataset } from "../api";

export default function DatasetBrowser(){
  const [years, setYears] = useState([]);
  const [year, setYear] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [preview, setPreview] = useState(null);

  useEffect(()=>{ fetchYears().then(j => { setYears(j.years||[]); if((j.years||[]).length) setYear(j.years[0]); }) }, []);
  useEffect(()=>{ if(year) fetchDatasetsByYear(year).then(j=>setDatasets(j.datasets||[])); }, [year]);

  const handlePreview = async (id) => { setPreview(await previewDataset(id)); };
  const handleDownload = async (id, filename) => {
    const blob = await downloadDataset(id);
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename || "dataset"; a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div>
      <h2>INGRES Datasets</h2>
      <select value={year||""} onChange={e=>setYear(Number(e.target.value))}>
        {years.map(y => <option key={y} value={y}>{y}</option>)}
      </select>
      <ul>
        {datasets.map(d=>(
          <li key={d.id}>
            <b>{d.name}</b> ({d.dataset_type})
            <button onClick={()=>handlePreview(d.id)}>Preview</button>
            <button onClick={()=>handleDownload(d.id,d.filename)}>Download</button>
          </li>
        ))}
      </ul>
      <pre>{preview && JSON.stringify(preview,null,2)}</pre>
    </div>
  );
}
