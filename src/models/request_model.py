from sqlalchemy import Column, String

from app.models.base_model import AbstractModel

class RequestModel(AbstractModel):
    data_id = Column(String, index=True)
    analysis_info = Column(String, default='{}')
