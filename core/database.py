from mysqlx import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import logger

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345678@localhost/flask"
# SQLALCHEMY_DATABASE_URI = "postgresql://root:123477777@localhost/database"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DB_OPS:
    def __init__(self, db: Session):
        self.db = db
    
    def fetch_all(self, model):
        try:
            records = self.db.query(model).all()
            return records
        except Exception as error:
            logger.error("DB_OPS", "fetch_all", str(error))
            return []
    
    def filter_fetch(self, model, conditions):
        try:
            query = self.db.query(model)
            conditions = dict(conditions)
            columns = list(conditions.keys())
            for col in columns:
                query = query.where(getattr(model, col).in_(conditions[col]))
            records = query.all()
            return records
        except Exception as error:
            logger.error("DB_OPS", "filter_fetch", str(error))
            return []
    
    def search_fetch(self, model, conditions):
        try:
            query = self.db.query(model)
            conditions = dict(conditions)
            columns = list(conditions.keys())
            for col in columns:
                query = query.where(getattr(model, col).like(f"%{conditions[col]}%"))
            records = query.all()
            return records
        except Exception as error:
            logger.error("DB_OPS", "search_fetch", str(error))
            return []
    
    def fetch_select_all(self, model):
        try:
            pass
        except Exception as error:
            logger.error("DB_OPS", "fetch_selected", str(error))
            return []