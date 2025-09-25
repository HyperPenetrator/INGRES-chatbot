const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

export async function fetchYears(){ 
  const r = await fetch(`${API_BASE}/datasets/years`);
  return r.json();
}
export async function fetchDatasetsByYear(year){
  const r = await fetch(`${API_BASE}/datasets?year=${year}`);
  return r.json();
}
export async function previewDataset(id){
  const r = await fetch(`${API_BASE}/datasets/${id}/preview`);
  return r.json();
}
export async function downloadDataset(id){
  const r = await fetch(`${API_BASE}/datasets/${id}/download`);
  const blob = await r.blob();
  return blob;
}
export async function uploadDataset(formData){
  const r = await fetch(`${API_BASE}/datasets/upload`, { method: "POST", body: formData });
  return r.json();
}
