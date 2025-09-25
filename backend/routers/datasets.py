from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import mimetypes, os, csv, json

from backend.models.dataset import Dataset
from backend.storage import save_upload_file
from backend.db import get_db

router = APIRouter(prefix="/api/datasets", tags=["datasets"])

@router.post("/upload")
async def upload_dataset(
    year: int = Query(..., ge=1900, le=2100),
    file: UploadFile = File(...),
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    filename = file.filename
    content_type = file.content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
    ext = filename.split(".")[-1].lower()
    if ext in ("csv", "txt"):
        dataset_type = "csv"
    elif ext in ("json", "geojson"):
        dataset_type = "geojson"
    elif ext in ("zip","shp","dbf"):
        dataset_type = "shapefile"
    elif ext == "pdf":
        dataset_type = "pdf"
    else:
        dataset_type = "other"

    saved_path, size = save_upload_file(file, year, filename)

    ds = Dataset(
        year=year,
        name=os.path.splitext(filename)[0],
        filename=saved_path,
        content_type=content_type,
        size_bytes=size,
        dataset_type=dataset_type,
        description=description
    )
    db.add(ds)
    db.commit()
    db.refresh(ds)
    return {"id": ds.id, "name": ds.name, "year": ds.year}

@router.get("/years")
def list_years(db: Session = Depends(get_db)):
    rows = db.query(Dataset.year).distinct().order_by(Dataset.year.desc()).all()
    years = [r[0] for r in rows]
    return {"years": years}

@router.get("/")
def list_by_year(year: int, db: Session = Depends(get_db)):
    rows = db.query(Dataset).filter(Dataset.year == year).order_by(Dataset.uploaded_at.desc()).all()
    return {"datasets": [
        {
            "id": r.id,
            "name": r.name,
            "filename": os.path.basename(r.filename),
            "dataset_type": r.dataset_type,
            "size_bytes": r.size_bytes,
            "uploaded_at": r.uploaded_at.isoformat(),
            "description": r.description
        } for r in rows
    ]}

@router.get("/{dataset_id}/download")
def download_dataset(dataset_id: str, db: Session = Depends(get_db)):
    ds = db.query(Dataset).get(dataset_id)
    if not ds:
        raise HTTPException(404, "not found")
    from fastapi.responses import FileResponse
    return FileResponse(path=ds.filename, filename=os.path.basename(ds.filename), media_type=ds.content_type)

@router.get("/{dataset_id}/preview")
def preview_dataset(dataset_id: str, rows: int = 10, db: Session = Depends(get_db)):
    ds = db.query(Dataset).get(dataset_id)
    if not ds:
        raise HTTPException(404, "not found")
    if ds.dataset_type == "csv":
        out = []
        with open(ds.filename, newline='', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            try: header = next(reader)
            except StopIteration: header = []
            out.append({"row": "header", "data": header})
            for i, r in enumerate(reader):
                if i >= rows: break
                out.append({"row": i+1, "data": r})
        return {"preview": out}
    elif ds.dataset_type == "geojson":
        with open(ds.filename, encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            feats = data.get("features", [])
            return {"features_count": len(feats), "features_preview": feats[:rows]}
    else:
        return {"message": "Preview not supported", "type": ds.dataset_type}
