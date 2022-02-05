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
        self.is_indexing = False
        self.current_index = None
        self.current_address = ''
        self.z = 10
        self.pt = None
        self.ll = [37.622513, 55.753220]
        self.current_visibility = 'map'
        self.l_number = 0
        self.static_map_params = {'l': self.current_visibility,
                                  'll': f'{str(self.ll[0])},{str(self.ll[1])}',
                                  'size': '640,450', 'z': str(self.z), 'pt': self.pt}
        self.geocoder_link = 'https://geocode-maps.yandex.ru/1.x'
        self.geocoder_params = {'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                'geocode': None, 'format': 'json'}
        self.image = None
        self.pixmap = None
        self.response = None
        self.map_radio.clicked.connect(self.change_visibility)
        self.sat_radio.clicked.connect(self.change_visibility)
        self.skl_radio.clicked.connect(self.change_visibility)
        self.postal_code_box.clicked.connect(self.change_indexing)
        self.search_button.clicked.connect(self.search)
        self.reset.clicked.connect(self.update_marker)
        self.static_map_request()
        self.set_pixmap()

    def change_indexing(self):
        if not self.postal_code_box.isChecked():
            self.is_indexing = False
            self.result_search.setText(self.current_address)
        else:
            self.is_indexing = True
            if self.current_index:
                self.result_search.setText(self.current_index + ', ' + self.current_address)

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
        self.response = self.response.json()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.z += 1
            if self.z > 17:
                self.z = 17
        if event.key() == Qt.Key_PageDown:
            self.z -= 1
            if self.z < 2:
                self.z = 2
        if event.key() == Qt.Key_Down:
            self.ll[1] -= 0.2
        if event.key() == Qt.Key_Up:
            self.ll[1] += 0.2
        if event.key() == Qt.Key_Left:
            self.ll[0] -= 0.2
        if event.key() == Qt.Key_Right:
            self.ll[0] += 0.2
        self.static_map_params['ll'] = f'{str(self.ll[0])},{str(self.ll[1])}'
        self.static_map_params['z'] = str(self.z)
        self.static_map_request()

    def search(self):
        self.geocoder_params['geocode'] = self.searching_line.text()
        self.geocoder_request()
        try:
            toponym = self.response["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            self.current_address = toponym_address
            toponym_coordinates = toponym["Point"]["pos"].split(' ')
            try:
                self.current_index = str(
                    self.response["response"]["GeoObjectCollection"]["featureMember"][0][
                        "GeoObject"][
                        'metaDataProperty']['GeocoderMetaData']['Address'][
                        'postal_code'])
            except KeyError:
                self.current_index = ''
            if toponym_address:
                self.ll = [float(toponym_coordinates[0]), float(toponym_coordinates[1])]
                self.static_map_params['ll'] = f'{str(self.ll[0])},{str(self.ll[1])}'
                self.static_map_request()
                self.update_marker('add')
                if self.is_indexing and self.current_index:
                    string = self.current_index + ', ' + toponym_address
                else:
                    string = toponym_address
                self.result_search.setText(string)
                if toponym_address:
                    self.ll = [float(toponym_coordinates[0]), float(toponym_coordinates[1])]
                    self.static_map_params['ll'] = f'{str(self.ll[0])},{str(self.ll[1])}'
                    self.static_map_request()
                    self.update_marker('add')
                self.searching_line.clear()
        except KeyError:
            self.current_index = ''

    def update_marker(self, action='clear'):
        if action == 'add':
            ll = f'{str(self.ll[0])},{str(self.ll[1])}'
            self.pt = ll + ',ya_ru'
        else:
            self.result_search.clear()
            self.searching_line.clear()
            self.pt = None
        self.static_map_params['pt'] = self.pt
        self.static_map_request()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
