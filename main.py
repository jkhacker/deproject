from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

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
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=5, height=4)
        m.move(0, 0)
        euler_button = QPushButton('Euler solution', self)
        euler_button.clicked.connect(m.plot)
        euler_button.move(500, 0)
        euler_button.resize(200, 50)

        eulerim_button = QPushButton('Euler Improved solution', self)
        eulerim_button.move(500, 50)
        eulerim_button.resize(200, 50)

        eulerim_button = QPushButton('Runge-Kutta solution', self)
        eulerim_button.move(500, 100)
        eulerim_button.resize(200, 50)

        self.show()
    
        


class PlotCanvas(FigureCanvas):

    sol = Solution()

    def __init__(self, parent=None, width=5, height=4, dpi=100, sol=Solution()):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.sol = sol

    def plot(self):
        self.sol.accuracy(100)
        data = self.sol.rungekutta()
        ax = self.figure.add_subplot(111)
        ax.plot(self.sol.xgrid(), data, 'r-')
        ax.set_title('y\'=(y^2 - y)/x')
        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
