import random

from essentials.json_util import json_open, json_dump


def create_house(path, config, region, author_id, house_name, house_type):
    house_json_path = f"{path}/database/residential/{author_id}/{house_name}.json"

    region_data = json_open(f"{path}/database/regions/{region}.json")

    region_state = region_data['parent']
    state_data = json_open(f"{path}/database/states/{region_state}.json")

    house_data = {
        "owner": author_id,
        "name": house_name,
        "region": region,
        "house_type": house_type,
        "cost": int(state_data[f"{house_type}_min"] * (1 + ((abs(random.randint(state_data[f"residential_weight"]-30, state_data[f"residential_weight"]+30)))/5000)**1.08))
    }
    region_data['residential'] += state_data[f"{house_type}_residential_score"]
    state_data['residential_weight'] += state_data[f"{house_type}_residential_weight"]

    json_dump(house_data, house_json_path)
    json_dump(region_data, f"{path}/database/regions/{region}.json")
    json_dump(state_data, f"{path}/database/states/{region_state}.json")

