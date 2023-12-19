"""
GUI
"""
from  PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic

import config
import control


class MainWindow(QWidget):  # default_size = (410, 300)
    def __init__(self):
        super().__init__()
        self.win = uic.loadUi('WeatherWidget.ui', self)
        # current
        self.cur_data = control.current_data()  # [0] icon [1] temp-c
        self.lb_cur_icon.setPixmap(self.cur_data[0])
        self.lb_cur_temp_c.setText('temp_c: ' + self.cur_data[1])
        # forecast
        self.forecast_apply()
        # extra
        self.lb_city.setText(control.city)

    def forecast_apply(self):
        days = self.win.fr_forecast.children()  # QFrames for each day
        for i in range(len(days)):  # QFrame of day i
            day_data = control.forecast_data(i)  # [0] date [1] temp_max [2] temp_min
            day_entries = days[i].children()  # should be same as above
            for j in range(len(day_entries)):  # day_entry j
                text = day_entries[j].text()
                day_entries[j].setText(text + day_data[j])  # output data to gui


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
