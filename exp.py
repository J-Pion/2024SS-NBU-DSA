from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
import os
import folium
import pandas as pd

distance = pd.read_excel(r".\城市空间最短路矩阵.xlsx",index_col = 0)
route = pd.read_excel(r".\城市空间最短路径矩阵.xlsx",index_col = 0)
location = []
loc = []
with open(r".\370_cities_CN_list.txt", 'r', encoding='ansi') as f:
    cities = f.readlines()
    cities = cities[1:]
    for city in cities:
        city = city.split(',')
        location.append([float(city[-1]), float(city[-2])])
        loc.append(city[3])
def get_shortest_path(origin, destination):
    dist = distance[destination][origin]
    path = route[destination][origin]
    path = path[1:-1]
    path = path.split(',')
    p = [ [location[int(i)][0], location[int(i)][1]] for i in path ]
    l = [loc[int(i)] for i in path]
    return p,dist,l

# 创建地图
Map = folium.Map(location=[29.910956,121.637222],
                 zoom_start=10,
                 tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                 attr='default')
Map.add_child(folium.LatLngPopup())
Map.save("save_map.html")

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('铁路规划')
        self.resize(1000, 1000)

        # 设置中心窗口
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 设置布局
        self.layout = QVBoxLayout(self.central_widget)

        # 输入出发地和目的地
        self.origin_input = QLineEdit(self)
        self.destination_input = QLineEdit(self)
        self.layout.addWidget(self.origin_input)
        self.layout.addWidget(self.destination_input)

        # 按钮点击事件
        self.button = QPushButton('显示路径', self)
        self.button.clicked.connect(self.show_path)
        self.layout.addWidget(self.button)

        # QWebEngineView
        self.qwebengine = QWebEngineView(self)
        self.layout.addWidget(self.qwebengine)

        self.label = QLabel(self)
        self.label.setFixedSize(800, 30)
        self.layout.addWidget(self.label)
        self.label1 = QLabel(self)
        self.label1.setFixedSize(900, 30)
        self.layout.addWidget(self.label1)


        # # 定时器
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_map)
        # self.timer.start(5000)  # 5秒更新一次
        path = "file:\\" + os.getcwd() + "\\save_map.html"
        path = path.replace('\\', '/')
        self.qwebengine.load(QUrl(path))

    def show_path(self):
        # 清除地图上的所有图层
        Map._layers = {}
        origin = self.origin_input.text()
        destination = self.destination_input.text()
        if origin and destination:
            # 获取路径
            path,dist,l = get_shortest_path(origin, destination)
            path1,dist1,l1 = get_shortest_path(origin, origin)
            path = path1+path
            # 在地图上绘制路径
            folium.PolyLine(path, color='blue').add_to(Map)
            bounds = [[min(lat for lat, _ in path), min(lon for _, lon in path)],
                      [max(lat for lat, _ in path), max(lon for _, lon in path)]]
            # 调整地图视图以适应路径的边界框
            Map.fit_bounds(bounds)
            # 保存地图
            Map.save("save_map.html")
            # 加载地图
            self.update_map()
            self.label.setText('最短距离：' + str(dist))
            self.label1.setText('最短路径：' + str(l))

    def update_map(self):
        path = "file:\\" + os.getcwd() + "\\save_map.html"
        path = path.replace('\\', '/')
        self.qwebengine.load(QUrl(path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
