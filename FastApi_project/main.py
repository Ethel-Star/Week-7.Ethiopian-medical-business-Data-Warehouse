from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, Base, get_db

app = FastAPI()

# Initialize Jinja2Templates for HTML templates
templates = Jinja2Templates(directory="templates")

# Mount static files (CSS, JS, etc.) folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "10 Academy: Artificial Intelligence Mastery", "name": "Ethel C."})

@app.get("/detections", response_model=list[schemas.DetectionSchema])
def read_detections(db: Session = Depends(get_db)):
    return crud.get_all_detections(db)

@app.get("/detections/{image_name}", response_model=list[schemas.DetectionSchema])
def read_detections_by_image(image_name: str, db: Session = Depends(get_db)):
    return crud.get_detections_by_image(db, image_name)

@app.get("/favicon.ico")
def favicon():
    return {}
