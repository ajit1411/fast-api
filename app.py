from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils import logger
from core import models, schemas
from core.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# create FastAPI instance
api = FastAPI()


# configure the middleware for the application
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["Authorization"],
    allow_methods=["*"],
    allow_credentials=True
)


# Database dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        logger.error("dependency", "get_db", str(error))
        db.close()


@api.get("/user")
def get_user(db: Session = Depends(get_db)):
    records = db.query(models.UserDetails).all()
    return {
        "status": True,
        "data": records,
        "error": None
    }