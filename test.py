import json
import os
import random

strwff = ""
for i in range(6000):
    a = random.randint(0, 200)
    b = random.randint(0, 200)
    strwff += f"[{a},{b}],"

print(strwff)




k=[3,4,2,5]
k.remove(7)