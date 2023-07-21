import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_colored_polygon(vertices_list, colors):
    """
    서로 다른 색으로 다각형 부분을 칠하는 함수
    :param vertices_list: (list) 각 부분을 이루는 꼭지점들의 좌표를 순서대로 담은 리스트들의 리스트
                          예: [[(x1, y1), (x2, y2), ..., (xn, yn)], ...]
    :param colors: (list) 각 부분에 대응하는 색상을 담은 리스트
                   예: ['red', 'green', 'blue', ...]
    """
    fig, ax = plt.subplots()

    for vertices, color in zip(vertices_list, colors):
        x, y = zip(*vertices)
        poly = patches.Polygon(list(zip(x, y)), facecolor=color)
        ax.add_patch(poly)

    ax.autoscale()
    ax.set_aspect('equal')
    plt.xlabel('X축')
    plt.ylabel('Y축')
    plt.title('다각형 색칠하기')
    plt.grid(True)
    plt.show()


# 다각형의 꼭지점들을 정의합니다.
vertices_list = [
    [(-36.07616, 46.49394), (-36.07616, 49.83463), (-33.96039, 54.06616), (-31.06513, 52.84124), (-26.55521, 53.28666),
     (-20.25948, 38.74361)],  # 첫 번째 부분
    [(-26.55521, 53.28666), (-17.42401, 67.1505), (-9.8754, 37.34933), (-20.25948, 38.74361)],  # 두 번째 부분
    [(-26.55521, 53.28666), (-30.95378, 56.29328), (-30.17428, 58.5204), (-31.78895, 59.57828), (-31.9003, 62.52922),
     (-34.29446, 63.30871),
     (-33.62632, 64.58931), (-30.11861, 67.26186), (-34.90692, 75.89195), (-33.29225, 76.44874), (-30.11861, 75.72492),
     (-27.39038, 75.55789),
     (-25.66436, 74.83407), (-21.87825, 74.88975), (-17.75808, 73.21941), (-16.47748, 71.04796), (-17.42401, 67.1505),
     (-26.55521, 53.28666)],
    [(-17.42401, 67.1505), (-12.24595, 65.70287), (-8.40416, 63.25304), (-3.78289, 69.09923), (-0.55356, 65.8699),
     (-2.39093, 64.81202), (-2.725, 60.69185)
        , (-6.17704, 57.35116), (-2.89204, 57.57387), (-0.83195, 55.90353), (-9.88639, 37.33902)],
    [(-9.88639, 37.33902), (-0.83195, 55.90353), (1.8406, 56.12625), (3.78933, 57.35116), (5.95743, 35.24787)],
    [(3.78933, 57.35116), (5, 60), (6.57323, 60.46913), (10.08095, 61.69405), (18.31755, 55.41681),
     (4.79316, 46.97876)],
    [(4.79316, 46.97876), (18.3, 55.4), (18.85046, 33.49947), (5.92888, 35.23221)]
]

# 각 부분에 대응하는 색상을 정의합니다.
colors = ['#703B2C', '#F2B7A7', '#F07D5E', '#70554D', "#BD634A", "#BD7D3A", "#F08162"]

# 다각형 부분을 서로 다른 색으로 칠합니다.
plot_colored_polygon(vertices_list, colors)
