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
        self.spn = [0.5, 0.5]
        self.ll = [37.622513, 55.753220]
        self.current_visibility = 'map'
        self.l_number = 0
        self.static_map_params = {'l': self.current_visibility,
                                  'll': f'{str(self.ll[0])},{str(self.ll[1])}',
                                  'size': '640,450', 'spn': f'{str(self.spn[0])},{str(self.spn[1])}'}
        self.geocoder_link = 'https://static-maps.yandex.ru/1.x'
        self.geocoder_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b', 'gecode': None,
                                'format': 'json'}
        self.image = None
        self.pixmap = None
        self.response = None
        self.map_radio.clicked.connect(self.change_visibility)
        self.sat_radio.clicked.connect(self.change_visibility)
        self.skl_radio.clicked.connect(self.change_visibility)
        self.static_map_request()
        self.set_pixmap()

    def change_visibility(self):
        if self.map_radio.isChecked():
            self.current_visibility = 'map'
        elif self.sat_radio.isChecked():
            self.current_visibility = 'sat'
        elif self.skl_radio.isChecked():
            self.current_visibility = 'sat,skl'
        self.static_map_params['l'] = self.current_visibility
        self.static_map_request()

    def static_map_request(self):
        self.image = requests.get(self.static_map_link, self.static_map_params).content
        with open('map.png', 'wb') as file:
            file.write(self.image)
        self.set_pixmap()

    def set_pixmap(self):
        self.pixmap = QPixmap('map.png')
        self.map_lablel.setPixmap(self.pixmap)

    def geocoder_request(self):
        self.response = requests.get(self.geocoder_link, self.geocoder_params)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn[0] -= 0.01
            self.spn[1] -= 0.01
            if self.spn[0] < 0 and self.spn[1] < 0:
                self.spn[0] = 0
                self.spn[1] = 0
        if event.key() == Qt.Key_PageDown:
            self.spn[0] += 0.01
            self.spn[1] += 0.01
            if self.spn[0] > 5 and self.spn[1] > 5:
                self.spn[0] = 5
                self.spn[1] = 5
        if event.key() == Qt.Key_Down:
            self.ll[1] -= 0.1
        if event.key() == Qt.Key_Up:
            self.ll[1] += 0.1
        if event.key() == Qt.Key_Left:
            self.ll[0] -= 0.1
        if event.key() == Qt.Key_Right:
            self.ll[0] += 0.1
        self.static_map_params['ll'] = f'{str(self.ll[0])},{str(self.ll[1])}'
        self.static_map_params['spn'] = f'{str(self.spn[0])},{str(self.spn[1])}'
        self.static_map_request()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
