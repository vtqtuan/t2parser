from src.utils.singleton import Singleton
import uuid
import threading
import json

from src.db.database import create_request, update_request, get_request

class CachedRequest:
    def __init__(self):
        self._data_id = str(uuid.uuid4()).replace('-', '').lower()
        self._details = list()
        self._processing_time = -1
        self._resource_path = ''

    @property
    def data_id(self):
        return self._data_id
    
    @data_id.setter
    def data_id(self, value):
        if type(value) is not str:
            raise ValueError('The \'data_id\' should be str')
        self._data_id = value
    
    @property
    def details(self):
        return self._details
    
    @details.setter
    def details(self, value):
        if type(value) is not list:
            raise ValueError('The \'details\' should be list')
        self._details = value

    @property
    def processing_time(self):
        return self._processing_time
    
    @processing_time.setter
    def processing_time(self, value):
        if type(value) is not float:
            raise ValueError('The \'processing_time\' should be float')
        self._processing_time = value

    @property
    def resource_path(self):
        return self._resource_path
    
    @resource_path.setter
    def resource_path(self, value):
        if type(value) is not str:
            raise ValueError('The \'resource_path\' should be str')
        self._resource_path = value

@Singleton
class SharedCaching:
    def __init__(self, queue_size: int = 10):
        self._cached = dict()
        self._limit_size = queue_size
        self._queue_size = 0
        self._lock = threading.Lock()

    def store_request(self) -> str:
        self._lock.acquire()
        try:
            self._queue_size += 1
            new_req = CachedRequest()
            self._cached[new_req.data_id] = new_req
        finally:
            self._lock.release()
            create_request(new_req.data_id)
            return new_req.data_id

    def remove_request(self, data_id: str = ''):
        self._lock.acquire()
        try:
            if data_id in self._cached.keys():
                self._queue_size -= 1
                self._cached.pop(data_id)
        finally:
            self._lock.release()

    def update_request(self, **kwargs) -> None:
        self._lock.acquire()
        try:
            data_id = kwargs['data_id']
            if data_id in self._cached.keys():
                self._cached[data_id].details = kwargs['details']
                self._cached[data_id].processing_time = float(kwargs['processing_time'])
        finally:
            self._lock.release()
            update_request(kwargs['data_id'], kwargs['details'], float(kwargs['processing_time']))
            

    def get_request(self, data_id: str = '') -> CachedRequest:
        self._lock.acquire()
        req = CachedRequest()
        try:
            if data_id in self._cached.keys():
                req.data_id = self._cached[data_id].data_id
                req.details = self._cached[data_id].details
                req.processing_time = float(self._cached[data_id].processing_time)

            else:
                db_req = get_request(data_id)
                req.data_id = db_req.data_id
                req.details = json.loads(db_req.details)
                req.processing_time = db_req.processing_time

        finally:
            self._lock.release()

        return req