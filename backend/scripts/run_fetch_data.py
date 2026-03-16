import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vejrdata.api_clients.dmi_api import DMI_API
from src.vejrdata.api_clients.spac_api import SpacAPI

def get_data_from_api(data_from, data_source, data_type, data_id):
    ''' should take a time parameter as input and then return everything after this time as json'''
    #### DMI DATA

    if data_source == 'dmi':

        datetime = data_from + '/..'
        dmi_api = DMI_API()
        res = dmi_api.get('/metObs/collections/observation/items', params={'datetime':datetime, 'parameterId': data_type, 'stationId':data_id})

        #print(json.dumps(res, indent = 4)) 
        return res

    #### SPAC DATA

    if data_source == 'spac':
        project_root = Path(__file__).resolve().parents[2]

        envpath = os.path.join(project_root, '.env')

        load_dotenv(dotenv_path=envpath)
        api_key = os.environ.get("API_KEY_SPAC")

        spac_api = SpacAPI(api_key)

        res = spac_api.get('/records', {'from': data_from, 'limit':2})

        return res
