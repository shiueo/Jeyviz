import random


def inflation_function(val):
    return (val / 5000) ** 1.75


def house_cost_function(minimum_cost, inflation):
    return int(
        minimum_cost
        * (1 + ((abs(random.randint(inflation - 30, inflation + 30))) / 5000) ** 1.13)
    )
