import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_colored_polygon(vertices_list, colors):
    fig, ax = plt.subplots(figsize=(6, 8))

    for vertices, color in zip(vertices_list, colors):
        x, y = zip(*vertices)

        poly = patches.Polygon(list(zip(x, y)), facecolor=color, edgecolor="white")
        ax.add_patch(poly)
        ax.set_facecolor("#121212")

    ax.autoscale()
    ax.set_aspect("equal")
    plt.title("Natzhashite Union")
    plt.grid(False)
    plt.savefig("map.png")
    plt.show()


# 다각형의 꼭지점들을 정의합니다.
vertices_list = [
    # Quadrian
    [
        (-36.07616, 46.49394),
        (-36.07616, 49.83463),
        (-33.96039, 54.06616),
        (-31.06513, 52.84124),
        (-26.55521, 53.28666),
        (-20.25948, 38.74361),
    ],  # Quonan
    [
        (-26.55521, 53.28666),
        (-17.42401, 67.1505),
        (-9.88, 37.35),
        (-20.25948, 38.74361),
    ],  # Quaxan
    [
        (-26.55521, 53.28666),
        (-30.95378, 56.29328),
        (-30.17428, 58.5204),
        (-31.78895, 59.57828),
        (-31.9003, 62.52922),
        (-34.29446, 63.30871),
        (-33.62632, 64.58931),
        (-30.11861, 67.26186),
        (-34.90692, 75.89195),
        (-33.29225, 76.44874),
        (-30.11861, 75.72492),
        (-27.39038, 75.55789),
        (-25.66436, 74.83407),
        (-21.87825, 74.88975),
        (-17.75808, 73.21941),
        (-16.47748, 71.04796),
        (-17.42401, 67.1505),
    ],  # Quartz
    [
        (-17.42401, 67.1505),
        (-12.24595, 65.70287),
        (-8.40416, 63.25304),
        (-3.78289, 69.09923),
        (-0.55356, 65.8699),
        (-2.39093, 64.81202),
        (-2.725, 60.69185),
        (-6.17704, 57.35116),
        (-2.89204, 57.57387),
        (-0.83195, 55.90353),
        (-9.88, 37.35),
    ],  # Quotin
    [
        (-0.83195, 55.90353),
        (1.8406, 56.12625),
        (3.78933, 57.35116),
        (4.79, 46.98),
        (5.93, 35.23),
        (-9.88, 37.35),
    ],
    # Quixotic
    [
        (4.79, 46.98),
        (3.78933, 57.35116),
        (5, 60),
        (6.57323, 60.46913),
        (10.08095, 61.69405),
        (18.3, 55.4),
    ],  # Qoniq
    [(4.79, 46.98), (18.3, 55.4), (18.85, 33.5), (5.93, 35.23)],  # Quadiv
    [(18.3, 55.4), (31.5, 45.3), (29.83, 32.03), (18.85, 33.5)],  # Qurix
    [
        (10.08095, 61.69405),
        (14.36816, 63.03032),
        (16.0385, 66.59372),
        (21.77334, 64.64499),
        (23.96347, 62.26298),
        (26.44842, 60.69509),
        (18.3, 55.4),
    ],  # Quinan
    [
        (18.3, 55.4),
        (26.44842, 60.69509),
        (27.95714, 58.86096),
        (30.29417, 60.31052),
        (32.09872, 60.75426),
        (32.45371, 59.36387),
        (34.37659, 57.79599),
        (32.1283, 57.47058),
        (33.90326, 55.28146),
        (32.48329, 53.1515),
        (31.5, 45.3),
    ],  # Quanb
    [
        (32.48329, 53.1515),
        (34.43575, 51.67237),
        (38.459, 51.19904),
        (38.07442, 49.24659),
        (39.19857, 46.52498),
        (40, 42),
        (31.5, 45.3),
    ],  # Qheonix
    [
        (31.5, 45.3),
        (40, 42),
        (41.09186, 40.25344),
        (39.84939, 39.3068),
        (39.8198, 37.23601),
        (38.96191, 35.43146),
        (36.83195, 33.92275),
        (37.03903, 32.02945),
        (36.65445, 31.11239),
        (29.83, 32.03),
    ],  # Quixotic
    # Ghranten
    [(5.93, 35.23), (18.85, 33.5), (18.78, 23.12), (6.27, 21.63)],
    [(18.85, 33.5), (29.83, 32.03), (31.25, 25.46), (18.78, 23.12)],
    [(6.27, 21.63), (18.78, 23.12), (18.7, 11.99), (6.64, 6.64)],
    [(18.78, 23.12), (31.25, 25.46), (32.8, 18.25), (29.07, 16.59), (18.7, 11.99)],
    [(29.83, 32.03), (36.65, 31.11), (40, 30), (41.09, 27.5), (31.25, 25.46)],
    [
        (31.25, 25.46),
        (41.09, 27.5),
        (43.1, 25.82),
        (43.07, 23.51),
        (42.13, 22.39),
        (32.8, 18.25),
    ],
    # Realmz
    [(6.64, 6.64), (18.7, 11.99), (22.14, 6.3), (10.71, 2.01)],
    [(10.71, 2.01), (22.14, 6.3), (25.69, 0.43), (15.02, -2.89)],
    [(18.7, 11.99), (29.07, 16.59), (32.85, 10.23), (22.14, 6.3)],
    [(22.14, 6.3), (32.85, 10.23), (37.15, 2.97), (25.69, 0.43)],
    [
        (29.07, 16.59),
        (32.8, 18.25),
        (42.13, 22.39),
        (42.84, 19.16),
        (44.46, 18.75),
        (44, 16),
        (44.94, 15.08),
        (32.85, 10.23),
    ],
    [
        (32.85, 10.23),
        (44.94, 15.08),
        (44.17, 11.5),
        (43.04, 10.43),
        (42.75, 9.37),
        (43.52, 8.87),
        (43.7, 7.59),
        (44.91, 6.47),
        (44.82, 5.29),
        (44.11, 4.52),
        (37.15, 2.97),
    ],
    # Esteny
    [(-9.88, 37.35), (5.93, 35.23), (-8.39, 23.61)],
    [(-8.39, 23.61), (5.93, 35.23), (6.27, 21.63), (6.64, 6.64)],
    [(-8.39, 23.61), (6.64, 6.64), (-3.35, 7.89), (-6.72, 8.32)],
    [(-8.39, 23.61), (-6.72, 8.32), (-11.8, 8.95), (-20.13, 10), (-20.2, 25.69)],
    [(-20.26, 38.74), (-9.88, 37.35), (-8.39, 23.61), (-20.2, 25.69)],
    # Rocktz
    [(25.69, 0.43), (32.96, -3.15), (30.75, -6.67)],
    [(25.69, 0.43), (37.15, 2.97), (39.38, -6.31), (32.96, -3.15)],
    [(37.15, 2.97), (44.11, 4.52), (41.48, -6.55), (39.38, -6.31)],
    [
        (44.11, 4.52),
        (44.52, 3.51),
        (47.6, 2.27),
        (48, 0),
        (48.43, -1.19),
        (41.48, -6.55),
    ],
    [
        (48.43, -1.19),
        (48.13, -3.11),
        (46.54, -8.79),
        (44.73, -10.87),
        (42.39, -9.36),
        (42.9, -8.38),
        (41.48, -6.55),
    ],
    [
        (30.75, -6.67),
        (32.96, -3.15),
        (39.38, -6.31),
        (38.67, -7.23),
        (40.44, -8.29),
        (40.03, -9.45),
        (38.25, -9.36),
        (36.36, -11.19),
        (35.44, -10.95),
        (34.24, -11.55),
    ],
    # Ashan
    [(-12.56, -6.42), (-4.32, -4.25), (10.68, -21.34), (-5.65, -21.39)],
    [(1.44, 3.75), (6.64, 6.64), (10.71, 2.01), (15.02, -2.89), (-4.32, -4.25)],
    [
        (-4.32, -4.25),
        (15.02, -2.89),
        (20.24, -18.53),
        (19.05, -18.94),
        (18, -20),
        (17.16, -19.47),
        (15.89, -19.74),
        (15.68, -20.81),
        (14.35, -21.46),
        (13.28, -24.24),
        (12.78, -22.46),
        (12, -22),
        (11.78, -21.28),
        (10.68, -21.34),
    ],
    [
        (15.02, -2.89),
        (25.69, 0.43),
        (26.98, -14.47),
        (26, -16),
        (25.65, -15.45),
        (24.56, -17.31),
        (22.72, -17.67),
        (22.6, -18.62),
        (21.36, -19.44),
        (20.24, -18.53),
    ],
    [
        (25.69, 0.43),
        (30.75, -6.67),
        (34.23, -11.55),
        (34.11, -12.64),
        (32.93, -13),
        (31.33, -13.23),
        (30.71, -12.7),
        (29.14, -13.26),
        (29.2, -14.74),
        (28.02, -15.36),
        (26.98, -14.47),
    ],
    # Cronokz
    [(-33.6, 10.54), (-23.49, -6.85), (-35.15, -1.26)],
    [(-33.6, 10.54), (-20.13, 10), (-23.49, -6.85)],
    [(-20.13, 10), (-23.49, -6.85), (-12.56, -6.42)],
    [(-12.56, -6.42), (-23.49, -6.85), (-5.65, -21.39)],
    [(-23.49, -6.85), (-5.65, -21.39), (-16.32, -21.33), (-32.09, -21.23)],
    [(-35.15, -1.26), (-23.49, -6.85), (-32.09, -21.23)],
    # Schtarn
    [(-20.13, 10), (-11.8, 8.95), (-16.69, 2.31)],
    [(-11.8, 8.95), (-16.59, 2.31), (-6.72, 8.32)],
    [(-16.59, 2.31), (-6.72, 8.32), (-14.96, -1.22)],
    [(-14.96, -1.22), (-6.72, 8.32), (-12.56, -6.42)],
    [(-6.72, 8.32), (-12.56, -6.42), (-3.35, 7.89)],
    [(-3.35, 7.89), (-12.56, -6.42), (-4.32, -4.25)],
    [(-3.35, 7.89), (-4.32, -4.25), (1.44, 3.75)],
    [(1.44, 3.75), (-3.35, 7.89), (6.64, 6.64)],
    # Novorsk
    [
        (-5.65, -21.39),
        (10.68, -21.34),
        (10.5, -22.58),
        (11.54, -23.26),
        (12.43, -26.34),
        (13.85, -27.11),
        (14.91, -28.08),
        (15.65, -28.08),
        (15.41, -29.09),
        (16.27, -29.83),
        (15.33, -30.98),
        (15.38, -32.14),
        (14.56, -32.76),
        (-5.68, -34.26),
    ],
    [
        (-5.68, -34.26),
        (14.56, -32.76),
        (15.03, -33.76),
        (15.98, -34.27),
        (16.01, -35.18),
        (16.66, -35.54),
        (16.92, -37.11),
        (17.66, -37.28),
        (17.81, -39.18),
        (18.9, -39.68),
        (19.41, -40.92),
        (7.14, -44.7),
        (-5.74, -48.67),
    ],
    [
        (7.14, -44.7),
        (10.15, -59.97),
        (27.45423, -48.02134),
        (27.36549, -46.60137),
        (26.21176, -45.47723),
        (24.9397, -45.3589),
        (24.55513, -44.20517),
        (22.66184, -42.60771),
        (22.45476, -41.57231),
        (21.53769, -40.744),
        (19.40774, -40.92149),
    ],
    [
        (10.15, -59.97),
        (27.45423, -48.02134),
        (28.48963, -48.84966),
        (28.78546, -48.34675),
        (29.88002, -48.4355),
        (30.79708, -50.09213),
        (31.71414, -49.94422),
        (33.19327, -52.56244),
        (32.75028, -55.52708),
        (31.76207, -57.29905),
        (28.86558, -56.00415),
        (27.87737, -56.68568),
        (27.53661, -60.02515),
        (25.45795, -61.59266),
        (23.34522, -61.76305),
        (22.28886, -62.37642),
        (21.64141, -63.36463),
        (20.68727, -63.39871),
        (19.15384, -65.00029),
        (19.09633, -65.89158),
        (20.44514, -67.28125),
        (21.46696, -68.7118),
        (22.28441, -70.71457),
        (21.30346, -71.65464),
        (21.26259, -72.88083),
        (22.77488, -72.75821),
        (23.5106, -74.47487),
        (22.28441, -77.47902),
        (19.48462, -75.3945),
        (20.11815, -74.80185),
        (19.3007, -74.18876),
        (18.52411, -73.45305),
        (17.09357, -73.5961),
        (16.8892, -74.43399),
        (15.72433, -74.45443),
        (14.94774, -73.24868),
        (12.63843, -73.3713),
        (12.59756, -72.34948),
    ],
    [
        (-5.74083, -48.66575),
        (7.14, -44.7),
        (10.15, -59.97),
        (12.59756, -72.34948),
        (11.45312, -73.1465),
        (11.69836, -74.84272),
        (8.84428, -74.28682),
        (7.20212, -75.43633),
        (4.68843, -75.04246),
        (1.4443, -77.10293),
        (-1.66832, -78.46196),
        (-3.99183, -78.37428),
        (-5.6139, -76.44533),
        (-8.02508, -75.17398),
        (-6.92265, -63.17918),
    ],
    # Tetrin
    [(-16.32, -21.33), (-5.65, -21.39), (-5.68, -34.26), (-13.28, -34.05)],
    [(-13.28, -34.05), (-5.68, -34.26), (-5.74, -48.67), (-14.54, -48.61)],
    [(-16.32, -21.33), (-32.09, -21.23), (-28.71, -33.64), (-13.28, -34.05)],
    [(-28.71, -33.64), (-13.28, -34.05), (-14.54, -48.61), (-24.64, -48.54)],
    [(-42.76, -21.17), (-32.09, -21.23), (-28.71, -33.64), (-45.36, -33.51)],
    [
        (-45.36, -33.51),
        (-28.71, -33.64),
        (-24.64, -48.54),
        (-39.61, -48.53),
        (-43.46, -46.44),
        (-45.09, -46.51),
        (-48, -46),
    ],
    [(-54.86, -21.1), (-42.76, -21.17), (-45.36, -33.51), (-55.45, -32.97)],
    [
        (-55.45, -32.97),
        (-45.36, -33.51),
        (-48, -46),
        (-49.0703, -44.51995),
        (-50.28887, -44.51995),
        (-51.69985, -45.35371),
        (-53.59184, -45.12923),
        (-54.81041, -45.48198),
        (-56, -44),
    ],
    [
        (-54.86, -21.1),
        (-55.45, -32.97),
        (-62.63493, -32.81524),
        (-64.39866, -31.24392),
        (-65.71343, -29.5764),
        (-66.89994, -27.42786),
        (-66.54719, -25.08692),
        (-66.29065, -24.18903),
        (-65.52103, -23.03459),
        (-64.33452, -21.59154),
        (-63.12, -21.05),
    ],
    [
        (-62.63493, -32.81524),
        (-55.45, -32.97),
        (-56, -44),
        (-57.72858, -44.90476),
        (-59.13955, -44.51995),
        (-59.33196, -43.49378),
        (-61.12775, -40.86423),
        (-60.80707, -40.28701),
        (-62.18599, -38.77983),
        (-63.53283, -38.65156),
        (-64, -38),
        (-63.08388, -35.66926),
    ],
    # Zhalka
    [
        (-24.64034, -48.54262),
        (-14.54, -48.61),
        (-5.74083, -48.66575),
        (-6.92265, -63.17918),
        (-30.69, -63.28),
    ],
    [
        (-30.69, -63.28),
        (-6.92265, -63.17918),
        (-8.02508, -75.17398),
        (-9.38411, -75.9631),
        (-10.96234, -75.91926),
        (-10.34858, -78.46196),
        (-11.92681, -80.47858),
        (-13.94344, -80.78546),
        (-13.8996, -79.33875),
        (-15.25863, -79.42643),
        (-15.60935, -77.54132),
        (-18.80965, -75.48086),
        (-22.27298, -77.32213),
        (-24.46497, -76.00694),
        (-30.60253, -75.21782),
        (-31.65468, -73.50807),
        (-35.03034, -73.85879),
    ],
    [
        (-39.61032, -48.52841),
        (-24.64034, -48.54262),
        (-30.69, -63.28),
        (-35.03034, -73.85879),
        (-36.08288, -75.59355),
        (-37.23731, -75.20874),
        (-39.96307, -75.17667),
        (-41.05337, -76.0425),
        (-42.94537, -76.0425),
        (-43.68292, -75.2408),
        (-44.80529, -75.40114),
        (-45.63905, -76.36317),
        (-46.9859, -76.42731),
        (-48.52515, -74.18257),
        (-48.55721, -72.93193),
        (-48.39687, -70.23824),
        (-47.49898, -68.15384),
        (-48, -66),
        (-47.05003, -63.76057),
        (-46.02386, -60.81034),
        (-45.44665, -58.21286),
        (-44.51668, -55.23056),
        (-42.43228, -52.69721),
        (-40.66856, -50.51661),
    ],
    # Khachlen
    [(-45.09, 11), (-33.6, 10.54), (-35.15097, -1.25616)],
    [(-35.15097, -1.25616), (-32.09, -21.23), (-42.76, -21.17)],
    [(-45.09, 11), (-56.19, -3.37), (-35.15097, -1.25616)],
    [(-35.15097, -1.25616), (-56.19, -3.37), (-42.76, -21.17)],
    [(-45.09, 11), (-59.07542, 11.56646), (-56.19, -3.37)],
    [(-56.19, -3.37), (-54.86, -21.1), (-42.76, -21.17)],
    [
        (-59.07542, 11.56646),
        (-61.32016, 11.08544),
        (-62.60287, 10.31582),
        (-66.03411, 10.37996),
        (-68.63159, 10.31582),
        (-69.20881, 8.29555),
        (-68.40712, 6.98078),
        (-66.6434, 4.5757),
        (-66, 0),
        (-67.60543, -2.5754),
        (-67.28475, -4.21085),
        (-66.48306, -4.40325),
        (-56.19, -3.37),
    ],
    [
        (-56.19, -3.37),
        (-66.48306, -4.40325),
        (-66.99614, -5.20495),
        (-69.62569, -6.51972),
        (-69.65776, -8.18724),
        (-68, -8),
        (-68.21471, -8.95687),
        (-67.41302, -9.14927),
        (-67.25268, -9.85476),
        (-68.27885, -10.65646),
        (-68.27885, -11.81089),
        (-68.21471, -12.90119),
        (-67.02821, -13.31808),
        (-65.90584, -15.2742),
        (-65.8417, -17.10206),
        (-64, -18),
        (-63.78937, -19.63541),
        (-63.11595, -21.04639),
        (-54.86, -21.1),
    ],
    # Utenie
    [(-20.25948, 38.74361), (-36.07616, 46.49394), (-34.8, 28), (-20.2, 25.69)],
    [(-34.8, 28), (-20.2, 25.69), (-20.13384, 10), (-33.6, 10.54)],
    [
        (-34.8, 28),
        (-33.6, 10.54),
        (-59.07542, 11.56646),
        (-60, 14),
        (-59.36403, 15.31838),
        (-57.82478, 15.51079),
        (-55.03489, 18.33274),
        (-54.45767, 20.9623),
        (-56.02899, 23.20704),
        (-57.69651, 22.79016),
        (-60, 24),
        (-59.13955, 25.3235),
        (-58.94715, 26.67035),
        (-55.22729, 26.70241),
        (-54.89534, 27.5634),
        (-54.33856, 31.46087),
    ],
    [
        (-36.07616, 46.49394),
        (-34.8, 28),
        (-54.33856, 31.46087),
        (-52.55686, 34.52316),
        (-53.225, 37.14003),
        (-52.77957, 39.14444),
        (-55.17373, 43.8214),
        (-54.44992, 46.66098),
        (-52.11144, 49.22217),
        (-42.8132, 50.11302),
        (-41.19854, 47.16208),
        (-38.47031, 47.55183),
    ],
]

# 각 부분에 대응하는 색상을 정의합니다.
colors = (
    [
        "#6e3c17",
        "#683916",
        "#633614",
        "#5d3213",
        "#572f12",
        "#512c11",
        "#4b2910",
        "#46260e",
        "#40230d",
        "#3a200c",
        "#341c0b",
        "#2e190a",
    ]
    + ["#d4778f", "#cb5b78", "#c33f61", "#a83552", "#8c2c45", "#702337"]
    + ["#bc645e", "#b1504a", "#9b4641", "#853c37", "#6e322e", "#582825"]
    + ["#ecc377", "#e7b355", "#e3a432", "#d0901d", "#ad7818"]
    + ["#85a68e", "#72987d", "#62866c", "#54735d", "#46604d", "#384d3e"]
    + ["#61d4bd", "#64c8b4", "#68bbaa", "#6daea1", "#729f96"]
    + ["#9f76a8", "#9a77a2", "#95799b", "#907a95", "#8b7c8e", "#867e87"]
    + [
        "#f61257",
        "#ed1a5a",
        "#e5235d",
        "#dc2b60",
        "#d33363",
        "#ca3b66",
        "#c1446a",
        "#b84c6d",
    ]
    + ["#9fd58a", "#98ca85", "#92be82", "#8db07f", "#88a17e"]
    + [
        "#8a97d6",
        "#8795d1",
        "#8592cc",
        "#8490c7",
        "#828ec2",
        "#818cbc",
        "#808ab7",
        "#7f88b1",
        "#7f86aa",
        "#7e85a4",
    ]
    + ["#d36f1f", "#b9753e", "#9d7a5f"]
    + [
        "#cfacf0",
        "#c8a3ea",
        "#c19ce4",
        "#ba95dc",
        "#b38fd4",
        "#ac8acb",
        "#a486c0",
        "#9d83b5",
    ]
    + ["#9b6aec", "#8549e7", "#6e27e3", "#5d1aca"]
)

region_names = (
    [
        "Quartz",
        "Quonan",
        "Quaxan",
        "Quotin",
        "Quixotic",
        "Qoniq",
        "Quadiv",
        "Qualz",
        "Qurix",
        "Quinan",
        "Quanb",
        "Qheonix",
    ]
    + ["Ghranten", "Guano", "Goetia", "Ginah", "Guten", "Gallery"]
    + ["Reamal", "Reanan", "Reakov", "Reaqeo", "Realch", "Reaaav"]
    + ["Esnore", "Eubikan", "Enchan", "Epnoq", "Exhan"]
    + ["Rozen", "Rewin", "Rivinov", "Rafless", "Rivnow", "Riken"]
    + ["Asinz", "Arctan", "Arena", "Alljan", "Anoyz"]
    + ["Crontal", "Creitz", "Croval", "Crino", "Cryak", "Cranahk"]
    + [
        "Schartz",
        "Scherent",
        "Schuika",
        "Schuah",
        "Schwav",
        "Schury",
        "Scholp",
        "Schaki",
    ]
    + ["Nortsin", "Nork", "NVIDIWA", "Navian", "Nickan"]
    + [
        "Texin",
        "Tetanan",
        "Teron",
        "Tekinszi",
        "Tewey",
        "Tweety",
        "Tehani",
        "Turing",
        "Trewniq",
        "TQDM",
    ]
    + ["Zhkalaten", "Zhewy", "Zhantenq"]
    + ["Khronov", "Khzec", "Kintel", "Korean", "Khacy", "Kharzen", "Kouo", "Kew"]
    + ["Utah", "Uraniuw", "Untershat", "Uzi"]
)

# 다각형 부분을 서로 다른 색으로 칠합니다.
plot_colored_polygon(vertices_list, colors)
