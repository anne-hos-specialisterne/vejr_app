import os

from src.api_clients.spac_api import SpacAPI
from src.transformers.transform_data import transform_spac
from src.db_utils.postgres_db import insert_request_info_in_db, append_df_to_postgres


def spac_pipeline(timefrom, conn):

    # fetch data from Spac API
    api_key = os.environ.get("API_KEY_SPAC")

    spac_api = SpacAPI(api_key)

    res_json = spac_api.get('/records', {'from': timefrom})


    # transform data for database
    res_df = transform_spac(api_out_json=res_json)

    # write data to dabase
    request_id = insert_request_info_in_db(df = res_df, conn = conn)

    res_df['request_id'] = request_id
    append_df_to_postgres(df=res_df, table_name='observation', conn=conn)

    # DONE
    print(f'SPAC data added')