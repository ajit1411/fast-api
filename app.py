from base64 import encode
from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from core.database import DB_OPS
from utils.helper import generate_random_string
from utils import logger
from core import models
from core.models import Tasks
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


@api.get("/user/info")
def get_user(response: Response, db: Session = Depends(get_db)):
    try:
        records = db.query(models.UserDetails).all()
        return {
            "status": True,
            "data": records,
            "error": None
        }
    except Exception as error:
        response.status_code = status.HTTP_501_NOT_IMPLEMENTED
        return {
            "status": False,
            "data": {},
            "error": str(error)
        }

# --------- PROJECTS APIs --------- #

# FETCH USERS TASKS
@api.get("/user/task/all")
async def fetch_users_tasks(response: Response, db: Session = Depends(get_db)):
    try:
        dbs = DB_OPS(db)
        records = dbs.fetch_all(Tasks)
        return {
            "status": True,
            "data": records,
            "error": None
        }
    except Exception as error:
        response.status_code = status.HTTP_501_NOT_IMPLEMENTED
        return {
            "status": False,
            "data": [],
            "error": str(error)
        }

# CREATE USER TASKS
@api.post("/user/task/new")
async def create_new_task(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        req_body = await request.json()
        if not req_body:
            raise Exception("Invalid Json")
        req_body = dict(req_body)
        task_id = generate_random_string()
        task_title = req_body.get("title", "Not Given")
        task_descr = req_body.get("title", "Not Given")
        task = Tasks(task_id=task_id, title=task_title, description=task_descr, assigned_to="username", status=0)
        db.add(task)
        db.commit()
        return {
            "status": True,
            "data": {
                "task-id": task_id
            },
            "error": None
        }
    except Exception as error:
        logger.error("/user/task/new", "create_new_task", str(error))
        response.status_code = status.HTTP_501_NOT_IMPLEMENTED
        return {
            "status": False,
            "data": None,
            "error": str(error)
        }