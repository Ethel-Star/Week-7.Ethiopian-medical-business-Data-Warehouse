from pydantic import BaseModel

class DetectionSchema(BaseModel):
    id: int
    image_name: str
    class_name: str
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_w: float
    bbox_h: float

    class Config:
        orm_mode = True
