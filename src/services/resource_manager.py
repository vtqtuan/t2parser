import io
import os
import re
from src.utils.singleton import Singleton
from fastapi import File, UploadFile

@Singleton
class ResourceManager:
    def __init__(self, path: str = ''):
        self._path = path
        self._chunk_size = 1024 * 1024

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        if type(value) is not str:
            raise ValueError('The \'path\' should be str')
        self._path = value
    
    async def store_file(self, data_id, file: UploadFile = File(...)):
        stored_path = os.path.join(self.path, 'file_{id}'.format(id=data_id))

        try:
            with io.open(stored_path, 'wb') as f:
                while contents := await file.read(self._chunk_size):
                    f.write(contents)

        except Exception:
            return {"message": "There was an error storing the file"}
        
        finally:
            await file.close()

        return stored_path

    def delete_file(self, file_path):
        os.remove(file_path)

    def delete_file(self, data_id):
        stored_path = os.path.join(self.path, 'file_{id}'.format(id=data_id))
        try:
            os.remove(stored_path)
        except Exception:
            return
        
    def read_sentence(self, data_id):
        stored_path = os.path.join(self.path, 'file_{id}'.format(id=data_id))
        with io.open(stored_path, 'r', encoding='utf-8') as file:
            buffer = ""
            for line in file:
                buffer += line
                sentences = re.split(r'(?<=[.!?]) +', buffer)
                buffer = sentences.pop() if sentences else ""
                for sentence in sentences:
                    yield sentence.strip()
            
            if buffer:
                yield buffer.strip()