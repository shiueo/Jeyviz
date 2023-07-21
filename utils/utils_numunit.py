def number_formatter(v: str):
    return ",".join([v[max(i - 3, 0) : i] for i in range(len(str(v)), 0, -3)][::-1])
