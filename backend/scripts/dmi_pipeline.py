import os
import json

from src.api_clients.dmi_api import DMI_API
from src.api_data_validation.schemas import DMIdata
from src.transformers.transform_data import transform_dmi
from src.db_utils.postgres_db import insert_request_info_in_db, append_df_to_postgres


def dmi_pipeline(timefrom, parameter, location, conn):

    # fetch data from DMI API
    time_from = timefrom + '/..'
    dmi_api = DMI_API()
    res_json = dmi_api.get('/metObs/collections/observation/items', params={'datetime':time_from, 'parameterId': parameter, 'stationId':location, 'limit': 2})
    #print(json.dumps(res_json, indent = 4))

    data = DMIdata.model_validate(res_json)
    #print(data)

    # transform data for database
    res_df = transform_dmi(pydantic_data=data)
    #print(res_df)

    # write data to dabase
    request_id = insert_request_info_in_db(df = res_df, conn = conn)

    res_df['request_id'] = request_id
    append_df_to_postgres(df=res_df, table_name='observation', conn=conn)

    # DONE
    print(f'DMI data added for stationId {location}: {parameter}')