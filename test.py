import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 3D 그래프 생성
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 예시 vertices_list
vertices_list = [
    # Quadrian
    [(-36.07616, 46.49394, 0), (-36.07616, 49.83463, 0), (-33.96039, 54.06616, 0), (-31.06513, 52.84124, 0),
     (-26.55521, 53.28666, 0), (-20.25948, 38.74361, 0)],

    # Quonan
    [(5, 50, 0), (7, 53, 0), (8, 58, 0), (6, 60, 0), (4, 59, 0), (3, 54, 0)]
]

# 3D 도형을 그리기 위한 코드
polygons = [Poly3DCollection([vertices_list[0]], facecolors='cyan', edgecolors='blue', alpha=0.5),
            Poly3DCollection([vertices_list[1]], facecolors='lightgreen', edgecolors='green', alpha=0.5)]

# 그래프에 도형 추가
for poly in polygons:
    ax.add_collection3d(poly)

# 라벨 설정
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# 축 범위 설정
ax.set_xlim([-40, 10])
ax.set_ylim([35, 65])
ax.set_zlim([-5, 5])

# 그리드 표시
ax.grid()

# 그래프 보여주기
plt.tight_layout()
plt.show()
