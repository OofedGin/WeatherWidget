"""
UI
"""

import control

from PyQt6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QTimer
from io import BytesIO
import folium


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi('WeatherWidget2.ui', self)
        self.mapView = QWebEngineView()
        self.init_folium_map()
        self.icon = QIcon('icon.png')
        self.setWindowIcon(self.icon)
        # menu_actions
        self.win.actionQuit.triggered.connect(app.quit)
        self.win.actionRefresh.triggered.connect(self.refresh)
        self.win.actionReopen_Window.triggered.connect(self.show)
        # tray
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon('icon.png'))
        self.tray.setContextMenu(self.win.menuFile)
        # refresh
        self.refresh()
        # timer
        self.timer = QTimer()
        self.timer.setInterval(900000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()

    def refresh(self):
        def current_refresh():
            self.cur_data = control.weather_data('current')  # [0] icon [1] temp-c [2] last_updated
            self.lb_cur_icon.setPixmap(control.icon_request(self.cur_data[0]))
            self.lb_cur_temp_c.setText('temp_c: ' + self.cur_data[1])
            self.lb_last_upd.setText('last_updated: ' + self.cur_data[2][-6:])

        def forecast_refresh():
            days = self.win.fr_forecast.children()  # QFrames for each day
            for i in range(len(days)):  # QFrame of day i
                day_data = control.weather_data('forecast', i)  # [0] date [1] temp_max [2] temp_min
                day_entries = days[i].children()  # same as above
                for j in range(len(day_entries)):  # day_entry j
                    day_entries[j].setText(day_data[j])  # output data to ui

        current_refresh()
        forecast_refresh()
        print('refreshed successfully')

    def init_folium_map(self):
        data = BytesIO()
        folium_map = folium.Map(location=control.coords, zoom_start=12)
        folium.Marker(location=control.coords, popup=control.city).add_to(folium_map)
        folium_map.save(data, close_file=False)

        self.mapView.setHtml(data.getvalue().decode())
        self.mapView.setFixedSize(290, 280)
        self.mapView.setParent(self.win.fr_map)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.show()
    app.lastWindowClosed.connect(window.tray.show)
    sys.exit(app.exec())
