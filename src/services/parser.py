from underthesea import pos_tag
from py_vncorenlp import VnCoreNLP
from fastapi import File, UploadFile
from src.services.resource_manager import ResourceManager
import time
import threading

VN_CORE_NLP_MODEL = VnCoreNLP(save_dir='.', annotators=["pos"])
VN_CORE_NLP_MODEL_LOCK = threading.Lock()

class Parser:
    def __init__(self, model: str = 'underthesea') -> None:
        self.model = model
        self.processing_time = -1
        self.details = []
    
    def execute(self, content: str = '') -> None:
        # Parse with underthesea
        if self.model == 'underthesea':
            start_time = time.time()
            out_details = pos_tag(content)
            # Handle details
            for parsed_detail in out_details:
                temp_detail = dict()

                temp_detail["chunk"] = parsed_detail[0]
                temp_detail["tag"] = parsed_detail[-1]

                self.details.append(temp_detail)

            end_time = time.time()
            self.processing_time = (end_time - start_time) * 1000

        # Parse with VnCoreNLP
        else:
            start_time = time.time()
            
            VN_CORE_NLP_MODEL_LOCK.acquire()
            out_details = VN_CORE_NLP_MODEL.annotate_text(content.decode('utf-8'))
            VN_CORE_NLP_MODEL_LOCK.release()

            # Handle details
            for sentence_details in out_details.values():
                for parsed_detail in sentence_details:
                    temp_detail = dict()

                    temp_detail["chunk"] = parsed_detail['wordForm'].replace('_', ' ')
                    temp_detail["tag"] = parsed_detail['posTag']

                    self.details.append(temp_detail)

            end_time = time.time()
            self.processing_time = (end_time - start_time) * 1000


    def execute_file(self, data_id) -> None:
        if self.model == 'underthesea':
            start_time = time.time()

            for sentence in ResourceManager.Instance().read_sentence(data_id):
                out_details = pos_tag(sentence)
                # Handle details
                for parsed_detail in out_details:
                    temp_detail = dict()

                    temp_detail["chunk"] = parsed_detail[0]
                    temp_detail["tag"] = parsed_detail[-1]

                    self.details.append(temp_detail)

            end_time = time.time()
            self.processing_time = (end_time - start_time) * 1000

        else:
            start_time = time.time()

            VN_CORE_NLP_MODEL_LOCK.acquire()

            for sentence in ResourceManager.Instance().read_sentence(data_id):
                out_details = VN_CORE_NLP_MODEL.annotate_text(sentence)
                
                # Handle details
                for sentence_details in out_details.values():
                    for parsed_detail in sentence_details:
                        temp_detail = dict()

                        temp_detail["chunk"] = parsed_detail['wordForm'].replace('_', ' ')
                        temp_detail["tag"] = parsed_detail['posTag']

                        self.details.append(temp_detail)

            VN_CORE_NLP_MODEL_LOCK.release()

            end_time = time.time()
            self.processing_time = (end_time - start_time) * 1000

    def get_result(self):
        # Process is not done
        if self.processing_time <= -1:
            return [], -1
        return self.details, self.processing_time
