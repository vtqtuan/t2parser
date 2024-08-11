from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from underthesea import pos_tag
import py_vncorenlp

from src.services.parser import Parser
from src.services.caching import CachedRequest, SharedCaching

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=10)

router = APIRouter()

def handle_request(data):
    in_data_id = SharedCaching.Instance().store_request()

    parser = Parser(model='underthesea')
    parser.execute(data)
    res, time = parser.get_result()

    SharedCaching.Instance().update_request(data_id=in_data_id, details=res, processing_time=time)

    return SharedCaching.Instance().get_request(in_data_id)


"""
    Parse with input content
"""
@router.post('')
async def parse_content(request: Request):
    body = await request.body()
    
    future = executor.submit(handle_request, body)
    result = future.result()

    response = dict()
    response["data_id"] = result.data_id
    response["details"] = result.details
    response["processing_time"] = result.processing_time

    return response