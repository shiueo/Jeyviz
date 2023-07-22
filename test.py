import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_colored_polygon(vertices_list, colors, region_names):
    """
    서로 다른 색으로 다각형 부분을 칠하는 함수
    :param vertices_list: (list) 각 부분을 이루는 꼭지점들의 좌표를 순서대로 담은 리스트들의 리스트
                          예: [[(x1, y1), (x2, y2), ..., (xn, yn)], ...]
    :param colors: (list) 각 부분에 대응하는 색상을 담은 리스트
                   예: ['red', 'green', 'blue', ...]
    """
    fig, ax = plt.subplots()  # Change the background color to light gray

    for vertices, color, region_name in zip(vertices_list, colors, region_names):
        x, y = zip(*vertices)
        centroid_x = sum(x) / len(x)
        centroid_y = sum(y) / len(y)

        poly = patches.Polygon(list(zip(x, y)), facecolor=color, edgecolor="white")
        ax.add_patch(poly)

        plt.text(centroid_x, centroid_y, region_name, ha='center', va='center', fontweight='regular', color='#FFFFFF')

    ax.autoscale()
    ax.set_aspect('equal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Natzhashite Union')
    plt.grid(False)
    plt.show()

# Example usage
vertices_list = [[(1, 1), (2, 5), (7, 3)], [(3, 3), (6, 7), (8, 5), (5, 2)]]
colors = ['red', 'green']
region_names = ['Polygon 1', 'Polygon 2']
plot_colored_polygon(vertices_list, colors, region_names)
