import sys
import requests
from urllib3 import Retry
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from requests.adapters import HTTPAdapter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication


class MainWindow(QMainWindow):
    g_map: QLabel
    g_search: QLineEdit
    g_layer1: QPushButton
    g_layer2: QPushButton
    g_layer3: QPushButton
    editPerPress = 0.01

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
        self.zoomPerPress = 5
        self.ll = [48.295988, 42.061384]
        self.maptype = "map"

        self.map_key = ''
        self.map_point = ''

        self.g_search.returnPressed.connect(self.search)
        self.g_layer1.clicked.connect(self.mapTypeMap)
        self.g_layer2.clicked.connect(self.mapTypeSat)
        self.g_layer3.clicked.connect(self.mapTypeSatCKl)

        self.update()

    def mapTypeMap(self):
        self.maptype = 'map'
        self.update()

    def mapTypeSat(self):
        self.maptype = 'sat'
        self.update()

    def mapTypeSatCKl(self):
        self.maptype = 'sat,skl'
        self.update()
    
    def initUi(self):
        self.setObjectName("self")
        self.resize(964, 673)
        self.cwd = QtWidgets.QWidget(self)
        self.cwd.setObjectName("cwd")
        self.gridLayout = QtWidgets.QGridLayout(self.cwd)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.mapa = QtWidgets.QLabel(self.cwd)
        self.mapa.setObjectName("mapa")
        self.gridLayout.addWidget(self.mapa, 1, 0, 1, 1)
        self.g_search = QtWidgets.QLineEdit(self.cwd)
        self.g_search.setObjectName("g_search")
        self.gridLayout.addWidget(self.g_search, 0, 0, 1, 1)
        self.g_layer2 = QtWidgets.QPushButton(self.cwd)
        
        self.g_layer2.setObjectName("g_layer2")
        self.gridLayout.addWidget(self.g_layer2, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 2, 1)
        self.g_layer3 = QtWidgets.QPushButton(self.cwd)
        self.g_layer3.setObjectName("g_layer3")
        self.gridLayout.addWidget(self.g_layer3, 0, 4, 1, 1)
        self.g_layer1 = QtWidgets.QPushButton(self.cwd)
        self.g_layer1.setObjectName("g_layer1")
        self.gridLayout.addWidget(self.g_layer1, 0, 2, 1, 1)
        self.setCentralWidget(self.cwd)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 964, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Отображение карты"))
        self.mapa.setText(_translate("MainWindow", "TextLabel"))
        self.g_layer2.setText(_translate("MainWindow", "спутник"))
        self.g_layer3.setText(_translate("MainWindow", "гибрид"))
        self.g_layer1.setText(_translate("MainWindow", "смема"))

    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_W:
            if self.zoomPerPress < 17:
                self.zoomPerPress += 1
        elif key == Qt.Key_S:
            if self.zoomPerPress > 0:
                self.zoomPerPress -= 1

        elif key == Qt.Key_Escape:
            self.mapa.setFocus()

        elif key == Qt.Key_D:
            self.ll[0] += self.editPerPress
            if self.ll[0] > 180:
                self.ll[0] = self.ll[0] - 360
        elif key == Qt.Key_A:
            self.ll[0] -= self.editPerPress
            if self.ll[0] < 0:
                self.ll[0] = self.ll[0] + 360
        elif key == Qt.Key_E:
            if self.ll[1] + self.editPerPress < 90:
                self.ll[1] += self.editPerPress
        elif key == Qt.Key_Q:
            if self.ll[1] - self.editPerPress > -90:
                self.ll[1] -= self.editPerPress
        else:
            return

        self.update()

    def update(self):
        map_params = {
            "ll": f'{self.ll[0]},{self.ll[1]}',
            "l": self.maptype,
            'z': self.zoomPerPress,}
        session = requests.Session()
        if self.map_point:
            map_params['pt'] = self.map_point
        response = session.get('https://static-maps.yandex.ru/1.x/', params=map_params)
        with open('image.png', mode='wb') as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load('image.png')
        self.mapa.setPixmap(pixmap)

    def search(self):
        x, y = self.getGeo(self.g_search.text())
        if x == -1 or y == -1:
            return
        self.ll = [x, y]
        self.map_point = f'{x},{y},comma'
        self.update()
    
    def getGeo(self, toponym):
        params = {
            "apikey": "7d42a436-37e1-41f5-b92a-c61cca026788",
            "geocode": toponym,
            "format": "json"}
        
        session = requests.Session()
        response = session.get("http://geocode-maps.yandex.ru/1.x/", params=params)
        if not response:
            print("Ошибка")
            return 0, 0
        return list(map(float, response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()))
    


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())