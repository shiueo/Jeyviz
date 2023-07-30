import random

states = [
    "Schtarn",
    "Ashan",
    "Cronokz",
    "Novorsk",
    "Tetrin",
    "Zhalka",
    "Utenie",
    "Ghranten",
    "Khachlen",
    "Rocktz",
    "Realmz",
    "Esteny",
    "Quadrian",
]
residential_types = ["단독주택", "연립주택", "아파트", "별장", "테라스하우스", "원룸", "반지하"]

jsonstring = ""
for state in states:
    jsonstring += f'"__{state}_law_residential_min__":"-----------------------------------------------------------------------------------------------------",\n'
    for residential_type in residential_types:
        val = random.randint(200000, 800000)
        jsonstring += f'"{state}_{residential_type}_min": {val},\n'
        jsonstring += f'"{state}_{residential_type}_residential_score": {round(val/10000, 2)},\n'
print(jsonstring)
