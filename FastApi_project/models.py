from sqlalchemy import Column, Integer, String, DECIMAL
from database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    confidence = Column(DECIMAL)
    bbox_x = Column(DECIMAL)
    bbox_y = Column(DECIMAL)
    bbox_w = Column(DECIMAL)
    bbox_h = Column(DECIMAL)

