import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vejrdata.transformers.transform_data import transform_dmi, transform_spac

def transform_data_to_db_format(data_source, api_out_json):
    print('called the transform_data_to_db_format function')

    if data_source == 'dmi':
        pd_df = transform_dmi(api_out_json=api_out_json)

    if data_source == 'spac':
        pd_df = transform_spac(api_out_json=api_out_json)

    return pd_df