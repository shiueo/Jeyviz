import json
import os.path
import shutil


def reset_system(path, config):
    log_message = []
    shutil.rmtree(f"{path}/database")

    os.mkdir(f"{path}/database")
    os.mkdir(f"{path}/database/regions")
    os.mkdir(f"{path}/database/states")
    os.mkdir(f"{path}/database/users")
    os.mkdir(f"{path}/database/viz")
    os.mkdir(f"{path}/database/residential")

    for region in config["regions"]:
        region_pos = eval(f"config['{region}_pos']")
        region_parent = eval(f"config['{region}_parent']")
        region_color = eval(f"config['{region}_color']")
        region_init_residential = eval(f"config['{region}_init_residential']")
        region_init_corporate = eval(f"config['{region}_init_corporate']")
        region_init_industrial = eval(f"config['{region}_init_industrial']")
        region_init_natural = eval(f"config['{region}_init_natural']")
        region_init_traffic = eval(f"config['{region}_init_traffic']")
        region_init_security = eval(f"config['{region}_init_security']")
        region_init_hospital = eval(f"config['{region}_init_hospital']")
        region_init_leisure = eval(f"config['{region}_init_leisure']")

        data = {
            "parent": region_parent,
            "pos": region_pos,
            "color": region_color,
            "residential": region_init_residential,
            "corporate": region_init_corporate,
            "industrial": region_init_industrial,
            "natural": region_init_natural,
            "traffic": region_init_traffic,
            "security": region_init_security,
            "hospital": region_init_hospital,
            "leisure": region_init_leisure,
        }
        with open(f"{path}/database/regions/{region}.json", "w", encoding="utf8") as f:
            json.dump(data, f, indent="\t", ensure_ascii=False)

    for state in config["states"]:
        state_init_detachedhouse_min = eval(f"config['{state}_단독주택_min']")
        state_init_detachedhouse_residential_score = eval(
            f"config['{state}_단독주택_residential_score']"
        )
        state_init_detachedhouse_residential_weight = eval(
            f"config['{state}_단독주택_residential_weight']"
        )

        state_init_townhouse_min = eval(f"config['{state}_연립주택_min']")
        state_init_townhouse_residential_score = eval(
            f"config['{state}_연립주택_residential_score']"
        )
        state_init_townhouse_residential_weight = eval(
            f"config['{state}_연립주택_residential_weight']"
        )

        state_init_apartment_min = eval(f"config['{state}_아파트_min']")
        state_init_apartment_residential_score = eval(
            f"config['{state}_아파트_residential_score']"
        )
        state_init_apartment_residential_weight = eval(
            f"config['{state}_아파트_residential_weight']"
        )

        state_init_cottage_min = eval(f"config['{state}_별장_min']")
        state_init_cottage_residential_score = eval(
            f"config['{state}_별장_residential_score']"
        )
        state_init_cottage_residential_weight = eval(
            f"config['{state}_별장_residential_weight']"
        )

        state_init_terracehouse_min = eval(f"config['{state}_테라스하우스_min']")
        state_init_terracehouse_residential_score = eval(
            f"config['{state}_테라스하우스_residential_score']"
        )
        state_init_terracehouse_residential_weight = eval(
            f"config['{state}_테라스하우스_residential_weight']"
        )

        state_init_oneroom_min = eval(f"config['{state}_원룸_min']")
        state_init_oneroom_residential_score = eval(
            f"config['{state}_원룸_residential_score']"
        )
        state_init_oneroom_residential_weight = eval(
            f"config['{state}_원룸_residential_weight']"
        )

        state_init_basementhouse_min = eval(f"config['{state}_반지하_min']")
        state_init_basementhouse_residential_score = eval(
            f"config['{state}_반지하_residential_score']"
        )
        state_init_basementhouse_residential_weight = eval(
            f"config['{state}_반지하_residential_weight']"
        )

        state_init_residential_weight = eval(f"config['{state}_residential_weight']")

        data = {
            "단독주택_min": state_init_detachedhouse_min,
            "단독주택_residential_score": state_init_detachedhouse_residential_score,
            "단독주택_residential_weight": state_init_detachedhouse_residential_weight,
            "연립주택_min": state_init_townhouse_min,
            "연립주택_residential_score": state_init_townhouse_residential_score,
            "연립주택_residential_weight": state_init_townhouse_residential_weight,
            "아파트_min": state_init_apartment_min,
            "아파트_residential_score": state_init_apartment_residential_score,
            "아파트_residential_weight": state_init_apartment_residential_weight,
            "별장_min": state_init_cottage_min,
            "별장_residential_score": state_init_cottage_residential_score,
            "별장_residential_weight": state_init_cottage_residential_weight,
            "테라스하우스_min": state_init_terracehouse_min,
            "테라스하우스_residential_score": state_init_terracehouse_residential_score,
            "테라스하우스_residential_weight": state_init_terracehouse_residential_weight,
            "원룸_min": state_init_oneroom_min,
            "원룸_residential_score": state_init_oneroom_residential_score,
            "원룸_residential_weight": state_init_oneroom_residential_weight,
            "반지하_min": state_init_basementhouse_min,
            "반지하_residential_score": state_init_basementhouse_residential_score,
            "반지하_residential_weight": state_init_basementhouse_residential_weight,
            "residential_weight": state_init_residential_weight,
        }
        with open(f"{path}/database/states/{state}.json", "w", encoding="utf8") as f:
            json.dump(data, f, indent="\t", ensure_ascii=False)

    return f"{len(config['regions'])}개의 하위 행정구역 초기화 완료. / {len(config['states'])}개의 주 초기화 완료."
