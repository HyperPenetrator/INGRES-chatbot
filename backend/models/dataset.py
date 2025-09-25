import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(String, primary_key=True, default=gen_uuid)
    year = Column(Integer, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    filename = Column(String(1024), nullable=False)
    content_type = Column(String(128))
    size_bytes = Column(Integer)
    dataset_type = Column(String(64))  # csv/geojson/shapefile/pdf/other
    description = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
