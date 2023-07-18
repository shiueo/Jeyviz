import json
import os
import random

strwff = ""
for i in range(8000):
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    strwff += f"[{a},{b}],"

print(strwff)