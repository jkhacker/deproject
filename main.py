from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QCheckBox, QSlider, QLabel, QLineEdit, QErrorMessage
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import random

from classes import *


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'Differential Equations Assignment'
        self.width = 700
        self.height = 400
        self.button = QPushButton('Draw plot', self)
        self.check_box_dict = {
            'exact': QCheckBox('Exact solution plot', self),
            'euler': QCheckBox('Euler approx plot', self),
            'eim': QCheckBox('Euler improved approx plot', self),
            'rk': QCheckBox('Runge-Kutta approx plot', self)}
        self.accuracy_label = QLabel('Accuracy (N): 50', self)
        self.accuracy_slider = QSlider(Qt.Horizontal, self)
        self.x0 = QLineEdit(self)
        self.y0 = QLineEdit(self)
        self.X = QLineEdit(self)
        self.graph_dict = {
            self.check_box_dict['exact']: ExactGraph('Exact solution'),
            self.check_box_dict['euler']: EulerGraph('Euler approximation'),
            self.check_box_dict['eim']: EulerImGraph('Euler improved approximation'),
            self.check_box_dict['rk']: RungeKuttaGraph('Runge-Kutta approximation')}
        self.graph_colors_dict = {
            self.check_box_dict['exact']: 'b-',
            self.check_box_dict['euler']: 'r-',
            self.check_box_dict['eim']: 'y-',
            self.check_box_dict['rk']: 'g-'}
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

        self.check_box_dict['exact'].move(505, 50)
        self.check_box_dict['exact'].resize(200, 25)

        self.check_box_dict['euler'].move(505, 75)
        self.check_box_dict['euler'].resize(200, 25)

        self.check_box_dict['eim'].move(505, 100)
        self.check_box_dict['eim'].resize(200, 25)

        self.check_box_dict['rk'].move(505, 125)
        self.check_box_dict['rk'].resize(200, 25)

        self.accuracy_label.move(510, 160)
        self.accuracy_label.resize(200, 25)

        self.accuracy_slider.setRange(1, 500)
        self.accuracy_slider.setValue(50)
        self.accuracy_slider.setTickInterval(1)
        self.accuracy_slider.move(510, 180)
        self.accuracy_slider.resize(150, 50)
        self.accuracy_slider.valueChanged.connect(self.accuracy_change)

        validator = QRegExpValidator(QRegExp(r'^\-?\d{1,3}(\.\d{1,3})*$'))

        self.x0.setAlignment(Qt.AlignLeft)
        self.x0.setMaxLength(7)
        self.x0.setText('1')
        self.x0.setValidator(validator)
        lx0 = QLabel('X0: ', self)
        lx0.move(510, 230)
        lx0.resize(20, 20)
        self.x0.move(550, 230)
        self.x0.resize(75, 20)

        self.y0.setAlignment(Qt.AlignLeft)
        self.y0.setMaxLength(7)
        self.y0.setText('0.5')
        self.y0.setValidator(validator)
        ly0 = QLabel('Y0: ', self)
        ly0.move(510, 260)
        ly0.resize(20, 20)
        self.y0.move(550, 260)
        self.y0.resize(75, 20)

        self.X.setAlignment(Qt.AlignLeft)
        self.X.setMaxLength(7)
        self.X.setText('9')
        self.X.setValidator(validator)
        lX = QLabel('X: ', self)
        lX.move(510, 290)
        lX.resize(20, 20)
        self.X.move(550, 290)
        self.X.resize(75, 20)

        self.show()

    def draw(self):
        x0 = float(self.x0.text())
        y0 = float(self.y0.text())
        X = float(self.X.text())
        if x0 > X:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage('X0 should be less than X')
            return
        self.canvas.clr()
        for graph in self.graph_dict.values():
            graph.recalculate(
                n=self.accuracy_slider.value(), x0=x0, y0=y0, X=X)
        
        for check in self.check_box_dict.values():
            if check.isChecked():
                xgrid, ygrid, name = self.graph_dict[check].get_grid()
                self.canvas.plot(
                    xgrid,
                    ygrid,
                    name,
                    self.graph_colors_dict[check])
    
    def accuracy_change(self):
        self.accuracy_label.setText('Accuracy (N): ' + str(self.accuracy_slider.value()) )

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_title('y\'=(y^2 - y)/x')

    def clr(self):
        self.ax.clear()
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_title('y\'=(y^2 - y)/x')
        self.draw()

    def plot(self, xgrid, ygrid, label, color):
        self.ax.plot(xgrid, ygrid, color, label=label)
        self.ax.legend(fontsize='small')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
