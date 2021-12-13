import json
import os
from datetime import datetime as dt

class DataSaver:
    views = []
    VIEWS = (
        'Algorithm', 
        # 'Basis',
        # 'Entity',
        # 'Report',
    ) 
    DATA = {
        'test': {
            'h1': 'head1',
            'h2': 'head2'}
    }
    WORKFLOW_DIR = os.path.abspath('workflow')
    FILE_NAME = 'Reversible_Device_1'

    def __init__(self, views):
        self.views = views

    def save(self, file_name=FILE_NAME, path=WORKFLOW_DIR):
        data = {key: self.views[key].get_data() for key in self.VIEWS}
        data['DateTime'] = str(dt.now())

        try:
            with open(f'{path}/{file_name}.json', '+w') as json_file:
                json.dump(data, json_file)
        except Exception as e:
            print(f'[SAVE ERROR]: {e}')
            raise
