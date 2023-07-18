def progressive_tax(val: int):
    if val < 8e6:
        ratio = 0
    elif val < 12e6:
        ratio = 0.06
    elif val < 46e6:
        ratio = 0.15
    elif val < 88e6:
        ratio = 0.24
    elif val < 150e6:
        ratio = 0.35
    elif val < 300e6:
        ratio = 0.38
    elif val < 500e6:
        ratio = 0.40
    elif val < 1e9:
        ratio = 0.42
    else:
        ratio = 0.45

    return ratio


