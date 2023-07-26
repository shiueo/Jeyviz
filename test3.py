input_str = "(5.93, 35.23), (18.85, 33.5), (18.78, 23.12), (6.27, 21.63)"
coordinates_tuple = [tuple(map(float, pair.strip('()').split(', '))) for pair in input_str.split('), ')]
print(coordinates_tuple)
