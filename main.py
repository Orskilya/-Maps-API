import requests
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('01.ui', self)
        self.static_map_link = 'https://static-maps.yandex.ru/1.x'
        self.static_map_params = {'l': 'map', 'll': None, 'z': 1, 'size': (1024, 768), 'pt': None}
        self.geocoder_link = 'https://static-maps.yandex.ru/1.x'
        self.geocoder_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b', 'gecode': None,
                                'format': 'json'}
        self.image = None
        self.response = None

    def static_map_request(self):
        self.image = requests.get(self.static_map_link, self.static_map_params)

    def geocoder_request(self):
        self.response = requests.get(self.geocoder_link, self.geocoder_params)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
