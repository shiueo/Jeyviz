import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_regions(state_name, path, config, region_list: list):
    fig, ax = plt.subplots()
    for region in region_list:
        poses = config[f"{region}_pos"]
        coordinates_tuple = [[tuple(map(float, pair.strip('()').split(', '))) for pair in poses.split('), ')]]
        colors = ["#6e3c17", "#683916", "#633614", "#5d3213",
                  "#572f12", "#512c11", "#4b2910",
                  "#46260e", "#40230d", "#3a200c", "#341c0b",
                  "#2e190a"]

        for vertices, color in zip(coordinates_tuple, colors):
            x, y = zip(*vertices)

            poly = patches.Polygon(list(zip(x, y)), facecolor=color, edgecolor="white")
            ax.add_patch(poly)
            ax.set_facecolor('#121212')

    other_regions = [x for x in config['regions'] if x not in region_list]
    for region in other_regions:
        poses = config[f"{region}_pos"]
        coordinates_tuple = [[tuple(map(float, pair.strip('()').split(', '))) for pair in poses.split('), ')]]

        for coords in coordinates_tuple:
            poly = patches.Polygon(coords, facecolor="#B5B5B5", edgecolor="white")
            ax.add_patch(poly)
            ax.set_facecolor('#121212')


    ax.autoscale()
    ax.set_aspect('equal')
    plt.title(f'{state_name}')
    plt.grid(False)
    plt.savefig(f"{path}/database/viz/{state_name}.png")
