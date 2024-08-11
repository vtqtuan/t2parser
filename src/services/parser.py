from underthesea import pos_tag
from py_vncorenlp import VnCoreNLP
import time

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
            self.processing_time = start_time - end_time

        # Parse with VnCoreNLP
        else:
            self.model = VnCoreNLP(save_dir='.', annotators=["pos"])
            start_time = time.time()

            out_details = self.model.annotate_text(content.decode('utf-8'))
            # Handle details
            for sentence_details in out_details.values():
                for parsed_detail in sentence_details:
                    temp_detail = dict()

                    temp_detail["chunk"] = parsed_detail['wordForm'].replace('_', ' ')
                    temp_detail["tag"] = parsed_detail['posTag']

                    self.details.append(temp_detail)

            end_time = time.time()
            self.processing_time = start_time - end_time

    def get_result(self):
        # Process is not done
        if self.processing_time <= -1:
            return [], -1
        return self.details, self.processing_time
