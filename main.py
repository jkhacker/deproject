from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QCheckBox, QSlider, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

import random

from ivp import Solution


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'Differential Equations Assignment'
        self.width = 700
        self.height = 400
        self.button = QPushButton('Draw plot', self)
        self.check_exact = QCheckBox('Exact solution plot', self)
        self.check_e = QCheckBox('Euler approx plot', self)
        self.check_eim = QCheckBox('Euler improved approx plot', self)
        self.check_rk = QCheckBox('Runge-Kutta approx plot', self)
        self.accuracy_label = QLabel('Accuracy (N): 50', self)
        self.accuracy_slider = QSlider(Qt.Horizontal, self)
        self.sol = Solution(n=100)
        self.canvas = PlotCanvas(self, width=5, height=4)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.canvas.move(0, 0)
        
        self.button.clicked.connect(self.draw)
        self.button.move(500, 0)
        self.button.resize(200, 50)

        self.check_exact.move(505, 50)
        self.check_exact.resize(200, 25)

        self.check_e.move(505, 75)
        self.check_e.resize(200, 25)

        self.check_eim.move(505, 100)
        self.check_eim.resize(200, 25)

        self.check_rk.move(505, 125)
        self.check_rk.resize(200, 25)

        self.accuracy_label.move(510, 160)
        self.accuracy_label.resize(200, 25)

        self.accuracy_slider.setRange(1, 100)
        self.accuracy_slider.setValue(50)
        self.accuracy_slider.setTickInterval(1)
        self.accuracy_slider.move(510, 180)
        self.accuracy_slider.resize(150, 50)
        self.accuracy_slider.valueChanged.connect(self.accuracy_change)

        self.show()

    def draw(self):
        self.canvas.clr()
        if self.check_exact.isChecked():
            self.canvas.plot(self.sol.get_x_grid(), self.sol.get_y_grid_exact(), color='b-')
        if self.check_e.isChecked():
            self.canvas.plot(self.sol.get_x_grid(), self.sol.get_y_grid_e())
        if self.check_eim.isChecked():
            self.canvas.plot(self.sol.get_x_grid(), self.sol.get_y_grid_eim())
        if self.check_rk.isChecked():
            self.canvas.plot(self.sol.get_x_grid(), self.sol.get_y_grid_rk())
    
    def accuracy_change(self):
        self.accuracy_label.setText('Accuracy (N): ' + str(self.accuracy_slider.value()) )

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, sol=Solution()):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('y\'=(y^2 - y)/x')

    def clr(self):
        self.ax.clear()
        self.ax.set_title('y\'=(y^2 - y)/x')
        self.draw()

    def plot(self, x_grid, y_grid, color='r-'):
        self.ax.plot(x_grid, y_grid, color)
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
