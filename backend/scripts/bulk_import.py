import os, shutil, time
from backend.db import SessionLocal, init_db
from backend.models.dataset import Dataset
from backend.storage import ensure_year_dir

def import_from_tree(root="data"):
    init_db()
    db = SessionLocal()
    for year_name in os.listdir(root):
        year_path = os.path.join(root, year_name)
        if not os.path.isdir(year_path): continue
        try: y = int(year_name)
        except: continue
        for fname in os.listdir(year_path):
            fpath = os.path.join(year_path, fname)
            if not os.path.isfile(fpath): continue
            target_dir = ensure_year_dir(y)
            dest = os.path.join(target_dir, fname)
            if os.path.exists(dest):
                dest = os.path.join(target_dir, f"{int(time.time())}_{fname}")
            shutil.copy2(fpath, dest)
            size = os.path.getsize(dest)
            ext = fname.split(".")[-1].lower()
            dtype = "csv" if ext in ("csv","txt") else "geojson" if ext in ("json","geojson") else "shapefile" if ext in ("zip","shp","dbf") else "other"
            ds = Dataset(year=y, name=os.path.splitext(fname)[0], filename=dest, size_bytes=size, dataset_type=dtype)
            db.add(ds)
    db.commit()
    db.close()

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else "data"
    import_from_tree(root)
    print("done")
