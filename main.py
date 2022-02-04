import requests
import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from interface import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class Example(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.static_map_link = 'https://static-maps.yandex.ru/1.x'
        self.static_map_params = {'l': 'sat', 'll': (55.753220, 37.622513), 'z': 5,
                                  'size': (1006, 703), 'key': '248120a9-95c1-65b2-8876-fdd3b462ff8d'}
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
