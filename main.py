import requests
import sys
from PyQt5.QtGui import QPixmap
from interface import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt


class Example(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.static_map_link = 'https://static-maps.yandex.ru/1.x'
        self.z = 10
        self.l_list = ['map', 'sat', 'skl']
        self.l_number = 0
        self.static_map_params = {'l': 'map', 'll': '37.622513,55.753220', 'size': '640,450', 'z': str(self.z)}
        self.geocoder_link = 'https://static-maps.yandex.ru/1.x'
        self.geocoder_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b', 'gecode': None,
                                'format': 'json'}
        self.image = None
        self.pixmap = None
        self.response = None
        self.static_map_request()
        self.set_pixmap()

    def static_map_request(self):
        self.image = requests.get(self.static_map_link, self.static_map_params).content
        with open('map.png', 'wb') as file:
            file.write(self.image)

    def set_pixmap(self):
        self.pixmap = QPixmap('map.png')
        self.map_lablel.setPixmap(self.pixmap)

    def geocoder_request(self):
        self.response = requests.get(self.geocoder_link, self.geocoder_params)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z += 1
            if self.z > 17:
                self.z = 17
        if event.key() == Qt.Key_PageDown:
            self.z -= 1
            if self.z < 1:
                self.z = 1
        self.static_map_params = {'l': 'map', 'll': '37.622513,55.753220', 'size': '640,450', 'z': str(self.z)}
        self.static_map_request()
        self.set_pixmap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
