from fastapi import APIRouter, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import JSONResponse

from src.services.parser import Parser
from src.services.caching import CachedRequest, SharedCaching
from src.services.resource_manager import ResourceManager

router = APIRouter()

def handle_request(in_data_id, data, in_model='underthesea'):
    parser = Parser(model=in_model)
    parser.execute(data)
    res, time = parser.get_result()

    SharedCaching.Instance().update_request(data_id=in_data_id, details=res, processing_time=time)

def handle_request_file(in_data_id, in_model='underthesea'):
    parser = Parser(model=in_model)
    parser.execute_file(in_data_id)
    res, time = parser.get_result()

    SharedCaching.Instance().update_request(data_id=in_data_id, details=res, processing_time=time)
    ResourceManager.Instance().delete_file(in_data_id)

"""
    Parse with input file
"""
@router.post('/file')
async def parse_file(request: Request, file: UploadFile, background_tasks: BackgroundTasks):
    data_id = SharedCaching.Instance().store_request()
    file_path = await ResourceManager.Instance().store_file(data_id, file)
    model = request.headers.get('model') # underthesea or vncorenlp
    background_tasks.add_task(handle_request_file, data_id, model)

    return {"data_id": "{id}".format(id=data_id)}

"""
    Parse with input content
"""
@router.post('')
async def parse_content(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    model = request.headers.get('model') # underthesea or vncorenlp
    
    data_id = SharedCaching.Instance().store_request()
    background_tasks.add_task(handle_request, data_id, body, model)

    return {"data_id": "{id}".format(id=data_id)}

"""
    Polling status with data_id
"""
@router.get('/{data_id}')
def fetch_status(data_id: str = ''):
    cached_req = SharedCaching.Instance().get_request(data_id)

    return {
        "data_id": "{id}".format(id=cached_req.data_id),
        "details": cached_req.details,
        "processing_time": cached_req.processing_time
    }