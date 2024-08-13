from sqlalchemy import Column, String, Float

from src.models.base import AbstractModel

class RequestModel(AbstractModel):
    __name__ = 'request'
    
    data_id = Column(String, index=True)
    details = Column(String, default='[]')
    processing_time = Column(Float, default=-1)