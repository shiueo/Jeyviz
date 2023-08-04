def format_number_with_units(number):
    res = []
    if number >= 1e24:
        res.append(str(int(number // 1e24)) + "자")
        number %= 1e24
    if number >= 1e20:
        res.append(str(int(number // 1e20)) + "해")
        number %= 1e20
    if number >= 1e16:
        res.append(str(int(number // 1e16)) + "경")
        number %= 1e16
    if number >= 1e12:
        res.append(str(int(number // 1e12)) + "조")
        number %= 1e12
    if number >= 1e8:
        res.append(str(int(number // 1e8)) + "억")
        number %= 1e8
    if number >= 1e4:
        res.append(str(int(number // 1e4)) + "만")
        number %= 1e4
    if number >= 1:
        res.append(str(int(number)))
    return ' '.join(res)


# Test
print(format_number_with_units(125487))
print(format_number_with_units(120000343333))
