import sys
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    movePerPress = 0.05
    def __init__(self):
        super().__init__()
        self.initUi()

        self.zoomPerPress = 5
        self.maptypel = [37.977751, 55.757718]
        self.maptype = 'map'
        self.map_key = ''
        self.map_point = ''

        self.g_search.returnPressed.connect(self.search)
        self.g_index.stateChanged.connect(self.update)
        self.g_layer1.clicked.connect(self.mapTypeMap)
        self.g_layer2.clicked.connect(self.mapTypeSat)
        self.g_layer3.clicked.connect(self.mapTypeSatCKl)
        self.g_reset.clicked.connect(self.reset)

        self.update()

    def initUi(self):
        self.resize(926, 649)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.g_layer3 = QtWidgets.QPushButton(self.centralwidget)
        self.g_layer3.setObjectName("g_layer3")
        self.gridLayout.addWidget(self.g_layer3, 0, 5, 1, 1)
        self.g_map = QtWidgets.QLabel(self.centralwidget)
        self.g_map.setObjectName("g_map")
        self.gridLayout.addWidget(self.g_map, 4, 0, 1, 1)
        self.g_layer2 = QtWidgets.QPushButton(self.centralwidget)
        self.g_layer2.setObjectName("g_layer2")
        self.gridLayout.addWidget(self.g_layer2, 1, 5, 1, 1)
        self.g_reset = QtWidgets.QPushButton(self.centralwidget)
        self.g_reset.setObjectName("g_reset")
        self.gridLayout.addWidget(self.g_reset, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.inform_map = QtWidgets.QLabel(self.centralwidget)
        self.inform_map.setText("")
        self.inform_map.setObjectName("inform_map")
        self.gridLayout.addWidget(self.inform_map, 5, 0, 1, 1)
        self.g_layer1 = QtWidgets.QPushButton(self.centralwidget)
        self.g_layer1.setObjectName("g_layer1")
        self.gridLayout.addWidget(self.g_layer1, 2, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 3, 5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 2, 3, 1)
        self.g_search = QtWidgets.QLineEdit(self.centralwidget)
        self.g_search.setObjectName("g_search")
        self.gridLayout.addWidget(self.g_search, 0, 0, 1, 1)
        self.g_index = QtWidgets.QCheckBox(self.centralwidget)
        self.g_index.setObjectName("g_index")
        self.gridLayout.addWidget(self.g_index, 3, 5, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 926, 43))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle("Отображение карты")
        self.g_layer3.setText("гибрид")
        self.g_map.setText("TextLabel")
        self.g_layer2.setText("спутник")
        self.g_reset.setText("сброс")
        self.g_layer1.setText("схема")
        self.g_index.setText("Почт. индекс")

    def mapTypeMap(self):
        self.maptype = 'map'
        self.update()

    def mapTypeSat(self):
        self.maptype = 'sat'
        self.update()

    def mapTypeSatCKl(self):
        self.maptype = 'sat,skl'
        self.update()

    def reset(self):
        self.g_search.clear()
        self.inform_map.clear()
        self.map_point = ''
        self.update()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Q:
            if self.zoomPerPress < 17:
                self.zoomPerPress += 1
        elif key == Qt.Key_E:
            if self.zoomPerPress > 0:
                self.zoomPerPress -= 1
        elif key == Qt.Key_Escape:
            self.g_map.setFocus()

        elif key == Qt.Key_D:
            self.maptypel[0] += self.movePerPress
            if self.maptypel[0] > 180:
                self.maptypel[0] = self.maptypel[0] - 360
        elif key == Qt.Key_A:
            self.maptypel[0] -= self.movePerPress
            if self.maptypel[0] < 0:
                self.maptypel[0] = self.maptypel[0] + 360
        elif key == Qt.Key_W:
            if self.maptypel[1] + self.movePerPress < 90:
                self.maptypel[1] += self.movePerPress
        elif key == Qt.Key_S:
            if self.maptypel[1] - self.movePerPress > -90:
                self.maptypel[1] -= self.movePerPress
        else:
            return

        self.update()

    def update(self):
        map_params = {
            "ll": f'{self.maptypel[0]},{self.maptypel[1]}',
            "l": self.maptype,
            'z': self.zoomPerPress,
        }
        if self.map_point:
            map_params['pt'] = self.map_point
        response = make_request('https://static-maps.yandex.ru/1.x/', params=map_params)
        if not response:
            return
        with open('image.png', mode='wb') as image:
            image.write(response.content)

        pixmap = QPixmap()
        pixmap.load('image.png')

        self.g_map.setPixmap(pixmap)
        if geo_locate(self.g_search.text(), inform_map=True) != (-1, -1):
            self.inform_map.setText(
                f'{geo_locate(self.g_search.text(), inform_map=True, index_map=self.g_index.checkState())}')

    def search(self):
        x, y = geo_locate(self.g_search.text())
        if x == -1 or y == -1:
            return
        self.maptypel = [x, y]
        self.map_point = f'{x},{y},comma'
        self.update()


def geo_locate(name, inform_map=False, index_map=False):
    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': name,
        'format': 'json'
    }
    response = make_request('http://geocode-maps.yandex.ru/1.x/', params=params)
    if not response:
        return -1, -1
    geo_objects = response.json()['response']["GeoObjectCollection"]["featureMember"]
    if not geo_objects:
        return -1, -1
    if inform_map:
        index = ""
        if index_map:
            index = geo_objects[0]["GeoObject"]['metaDataProperty']['GeocoderMetaData']['Address']. \
                get("postal_code", "")
            if index:
                index += ", "
        return index + geo_objects[0]["GeoObject"]['metaDataProperty']['GeocoderMetaData']['text']
    return list(map(float, geo_objects[0]["GeoObject"]["Point"]["pos"].split()))


def make_request(*args, **kwargs):
    session = requests.Session()
    return session.get(*args, **kwargs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
