import json
import os.path
import shutil


def reset_system(path, config):
    log_message = []
    if os.path.isdir(f"{path}/database/regions"):
        shutil.rmtree(f"{path}/database/regions")
    if os.path.isdir(f"{path}/database/states"):
        shutil.rmtree(f"{path}/database/states")
    if os.path.isdir(f"{path}/database/users"):
        shutil.rmtree(f"{path}/database/users")
        if os.path.isdir(f"{path}/database/viz"):
            shutil.rmtree(f"{path}/database/viz")

    os.mkdir(f"{path}/database/regions")
    os.mkdir(f"{path}/database/states")
    os.mkdir(f"{path}/database/users")
    os.mkdir(f"{path}/database/viz")

    for region in config['regions']:
        region_pos = eval(f"config['{region}_pos']")
        region_parent = eval(f"config['{region}_parent']")
        region_init_residential = eval(f"config['{region}_init_residential']")
        region_init_corporate = eval(f"config['{region}_init_corporate']")
        region_init_industrial = eval(f"config['{region}_init_industrial']")
        region_init_natural = eval(f"config['{region}_init_natural']")
        region_init_traffic = eval(f"config['{region}_init_traffic']")
        region_init_security = eval(f"config['{region}_init_security']")
        region_init_hospital = eval(f"config['{region}_init_hospital']")
        region_init_leisure = eval(f"config['{region}_init_leisure']")

        data = {
            'parent': region_parent,
            'pos': region_pos,
            'residential': region_init_residential,
            'corporate': region_init_corporate,
            'industrial': region_init_industrial,
            'natural': region_init_natural,
            'traffic': region_init_traffic,
            'security': region_init_security,
            'hospital': region_init_hospital,
            'leisure': region_init_leisure
        }
        with open(f"{path}/database/regions/{region}.json", 'w') as f:
            json.dump(data, f)

    return f"{len(config['regions'])}개의 지역 초기화 완료. / User 초기화 완료. / State 초기화 완료."
