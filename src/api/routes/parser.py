from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse

from src.services.parser import Parser
from src.services.caching import CachedRequest, SharedCaching

router = APIRouter()

def handle_request(in_data_id, data):
    parser = Parser(model='underthesea')
    parser.execute(data)
    res, time = parser.get_result()

    SharedCaching.Instance().update_request(data_id=in_data_id, details=res, processing_time=time)

"""
    Parse with input content
"""
@router.post('')
async def parse_content(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    
    data_id = SharedCaching.Instance().store_request()
    background_tasks.add_task(handle_request, data_id, body)

    response = dict()
    response["data_id"] = data_id

    return response

"""
    Polling status with data_id
"""
@router.get('/{data_id}')
def fetch_status(data_id: str = ''):
    cached_req = SharedCaching.Instance().get_request(data_id)

    response = dict()
    response["data_id"] = cached_req.data_id
    response["details"] = cached_req.details
    response["processing_time"] = cached_req.processing_time

    return response