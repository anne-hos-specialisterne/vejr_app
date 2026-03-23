import pandas as pd

def transform_spac(api_out_json):

    rows = []

    for record in api_out_json["records"]:
        base = {
            "source_id": record["id"],
            "observation_time": record["timestamp"]
        }

        # Extract sensor type and readings
        reading = record["reading"]
        sensor_type = list(reading.keys())[0]
        sensor_values = reading[sensor_type]

        row = base.copy()
        row["location_code"] = 'outside_' + sensor_type

        # Flatten sensor values
        for k, v in sensor_values.items():
            if k == 'device_name':
                continue

            if k == 'raw_reading':
                k = 'temperature'

            row['observation_type'] = k
            row['observation_value'] = v

            rows.append(row.copy())

    res = pd.DataFrame(rows)

    return res



def transform_dmi(pydantic_data):
    ''' function specific to data from DMI api'''

    df = pd.DataFrame(columns = ['source_id', 'location_code', 'observation_type', 'observation_time', 'observation_value'])

    for r in pydantic_data.features:

        dict = {}
        dict['source_id'] = r.id
        dict['location_code'] = r.properties.stationId
        dict['observation_type'] = r.properties.parameterId 
        dict['observation_time'] = r.properties.observed 
        dict['observation_value'] = r.properties.value

        temp = pd.DataFrame(dict, index = [0])

        df = pd.concat([df, temp], ignore_index=True)

    return df