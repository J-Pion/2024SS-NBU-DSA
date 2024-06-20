import pandas as pd

# 读取CSV文件
distance = pd.read_excel(r".\370城市空间距离权重矩阵_2019-94kf93ksq2.xlsx")
adjacency = pd.read_excel(r".\370城市空间邻接矩阵_2019-03lf95kgd3.xlsx")

distance = distance.values.tolist()
adjacency = adjacency.values.tolist()

distance = [item[1:] for item in distance]
adjacency = [item[1:] for item in adjacency]

route = [[[] for _ in range(len(adjacency))] for _ in range(len(adjacency))]

for i in range(len(adjacency)):
    for j in range(len(adjacency[i])):
        if adjacency[i][j] == 1:
            adjacency[i][j] = distance[i][j]
            route[i][j].append(j)
        else:
            adjacency[i][j] = 999999

for k in range(len(adjacency)):
    for i in range(len(adjacency)):
        for j in range(len(adjacency[i])):
            if adjacency[i][j] > adjacency[i][k] + adjacency[k][j]:
                adjacency[i][j] = adjacency[i][k] + adjacency[k][j]
                route[i][j] = route[i][k] + route[k][j]

for i in range(len(route)):
    for j in range(len(route[i])):
        route[i][j] = str(route[i][j])

adjacency = pd.DataFrame(adjacency)
adjacency.to_excel(r"C:\Users\10761\Desktop\城市空间最短路矩阵.xlsx")

route = pd.DataFrame(route)
route.to_excel(r"C:\Users\10761\Desktop\城市空间最短路径矩阵.xlsx")
