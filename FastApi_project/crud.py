from sqlalchemy.orm import Session
import models

def get_all_detections(db: Session):
    return db.query(models.Detection).all()

def get_detections_by_image(db: Session, image_name: str):
    return db.query(models.Detection).filter(models.Detection.image_name == image_name).all()
