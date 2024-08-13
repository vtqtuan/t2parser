import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

from src.models.request import RequestModel

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def create_request(in_data_id: str = ''):
    db_session = next(get_db())

    request = RequestModel(data_id=in_data_id)

    db_session.add(request)
    db_session.commit()
    db_session.refresh(request)

def update_request(in_data_id: str = '', in_details: list = [], in_processing_time: float = -1.0):
    db_session = next(get_db())

    request = db_session.query(RequestModel).filter(RequestModel.data_id == in_data_id).first()
    request.details = json.dumps(in_details)
    request.processing_time = in_processing_time

    db_session.commit()

def get_request(in_data_id: str = ''):
    return next(get_db()).query(RequestModel).filter(RequestModel.data_id == in_data_id).first()