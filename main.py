import sys
import requests
from urllib3 import Retry
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRect
from requests.adapters import HTTPAdapter
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    editPerPress = 0.01

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUi()
        self.zoomPerPress = 5
        self.ll = [48.295988, 42.061384]
        self.update()
    
    def initUi(self):
        self.setObjectName("self")
        self.resize(500, 480)
        self.cwd = QtWidgets.QWidget(self)
        self.gridLayout = QtWidgets.QGridLayout(self.cwd)
        self.mapa = QtWidgets.QLabel(self.cwd)
        self.gridLayout.addWidget(self.mapa, 0, 0, 1, 1)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer_item, 1, 0, 1, 1)
        spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacer_item1, 0, 1, 1, 1)
        self.setCentralWidget(self.cwd)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 964, 21))
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W and self.zoomPerPress < 17:
            self.zoomPerPress += 1
        if key == Qt.Key_S and self.zoomPerPress > 0:
            self.zoomPerPress -= 1
        if key == Qt.Key_A:
            self.ll[0] -= self.editPerPress
        if key == Qt.Key_D:
            self.ll[0] += self.editPerPress
        if key == Qt.Key_E:
            self.ll[1] += self.editPerPress
        if key == Qt.Key_Q:
            self.ll[1] -= self.editPerPress
        self.update()

    def update(self):
        map_params = {
            "ll": f'{self.ll[0]},{self.ll[1]}',
            "l": "map",
            'z': self.zoomPerPress,
            "apikey": "94f9def1-dd04-4246-9b62-80ffedf50965"}
        session = requests.Session()
        response = session.get('https://static-maps.yandex.ru/1.x/', params=map_params)
        with open('image.png', mode='wb') as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load('image.png')
        self.mapa.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())