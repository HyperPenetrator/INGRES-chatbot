import React, { useState } from "react";
import { uploadDataset } from "../api";

export default function UploadDataset(){
  const [year,setYear] = useState(new Date().getFullYear());
  const [file,setFile] = useState(null);
  const [desc,setDesc] = useState("");

  const submit = async(e)=>{
    e.preventDefault();
    if(!file) return alert("select file");
    const fd=new FormData();
    fd.append("year",year);
    fd.append("file",file);
    fd.append("description",desc);
    alert(JSON.stringify(await uploadDataset(fd)));
  };

  return (
    <form onSubmit={submit}>
      <input type="number" value={year} onChange={e=>setYear(e.target.value)} />
      <input type="file" onChange={e=>setFile(e.target.files[0])}/>
      <input type="text" placeholder="desc" value={desc} onChange={e=>setDesc(e.target.value)}/>
      <button>Upload</button>
    </form>
  );
}

