from base64 import encode
from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils.Auth import UserAuth
from utils.helper import generate_hash_from, generate_jwt
from core.database import DB_OPS
from utils.helper import generate_random_string
from utils import logger
from core import models
from core.models import Tasks, UserDetails
from core.database import SessionLocal, engine
from sqlalchemy import select
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

@api.post("/user/register")
async def register_user(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        req_body = await request.json()
        req_body = dict(req_body)
        if not req_body or len(req_body) < 1:
            raise Exception("Invalid request")
        username = req_body.get("username", None)
        email = req_body.get("email", None)
        password = req_body.get("password", None)
        if not username or not email or not password:
            raise Exception("Invalid credentials: No `username` or `email` or `password`")
        hashed_password = generate_hash_from(password)
        if not hashed_password:
            raise Exception("Error while hashing password")
        user = UserDetails(username=username, email=email, profile_img="default.png", password=hashed_password)
        db.add(user)
        db.commit()
        user_data = req_body
        del user_data["password"]
        user_token = generate_jwt(user_info=user_data)
        response.status_code = status.HTTP_201_CREATED
        return {
            "status": True,
            "data": {
                "message": "user created",
                "token": user_token
            },
            "error": None
        }
    except Exception as error:
        logger.error("/user/register", "register_user", str(error))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status": False,
            "error": str(error)
        }

@api.get("/user/info")
async def get_user(request: Request, response: Response, db: Session = Depends(get_db)):
    try:
        headers = request.headers
        auth_token = headers.get("authorization", None)
        if not auth_token:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            logger.error("/user/info", "get_user", "No token found")
            return {
                "status": False,
                "error": "Unauthorized"
            }
        user = UserAuth(auth_token)
        decoded = user.decode()
        if not decoded:
            raise Exception("Failed to decode")
        records = db.query(models.UserDetails).where(UserDetails.username==decoded["username"]).all()
        # record = db.query(models.UserDetails).where(UserDetails.username=="jadhav").all()
        if len(records) == 0:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "status": False,
                "error": "Unauthorized"
            }
        record = records[0]
        return {
            "status": True,
            "data": records,
            "record": record,
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