from graph import Graph
import numpy as np
from utils import *

class ExactGraph(Graph):

    def _Graph__func(self, x, c):
        try:
            res = exact_func(x, c)
        except (OverflowError, ZeroDivisionError) as e:
            res = np.nan
        threshold = 50
        res = np.ma.masked_less(res, -1*threshold)
        res = np.ma.masked_greater(res, threshold)
        return res

    def _Graph__calc(self):
        c = find_coef(self._Graph__x0, self._Graph__y0)
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(self._Graph__func(x_i, c))

class EulerGraph(Graph):

    def _Graph__calc(self):
        y_i = self._Graph__y0
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(y_i)
            y_i = y_i + self._Graph__grid_step*self._Graph__func(x_i, y_i)

class EulerImGraph(Graph):

    def _Graph__calc(self):
        y_i = self._Graph__y0
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(y_i)
            y_i = y_i + (self._Graph__grid_step/2)*(
                self._Graph__func(x_i, y_i) + self._Graph__func(
                    x_i + self._Graph__grid_step, y_i +
                    self._Graph__grid_step*self._Graph__func(x_i, y_i)
                )
            )

class RungeKuttaGraph(Graph):

    def _Graph__calc(self):
        y_i = self._Graph__y0
        for x_i in self._Graph__xgrid:
            self._Graph__ygrid.append(y_i)
            k1 = self._Graph__func(x_i, y_i)
            k2 = self._Graph__func(x_i + self._Graph__grid_step/2, y_i + k1*self._Graph__grid_step/2)
            k3 = self._Graph__func(x_i + self._Graph__grid_step/2, y_i + k2*self._Graph__grid_step/2)
            k4 = self._Graph__func(x_i + self._Graph__grid_step, y_i + k3*self._Graph__grid_step)
            y_i = y_i + self._Graph__grid_step*(k1 + 2*k2 + 2*k3 + k4)/6

class ErrorGraph:
    def __init__(self, exact_graph, approx_graph, name):

        self.__exact = exact_graph
        self.__approx = approx_graph
        self.__name = name
        self.__ygrid = [x1 - x2 for (x1, x2) in zip(self.__exact.get_grid()[1], self.__approx.get_grid()[1])]
        self.__xgrid = self.__exact.get_grid()[0]
    
    def recalculate(self, *args):
        self.__ygrid = [x1 - x2 for (x1, x2) in zip(self.__exact.get_grid()[1], self.__approx.get_grid()[1])]
        self.__xgrid = self.__exact.get_grid()[0]

    def get_grid(self):
        return self.__xgrid, self.__ygrid, self.__name

class TotalErrorGraph:
    def __init__(self, name, ApproxGraph, AnalGraph, x0=1, y0=0.5, X=9):
        self.__approx = ApproxGraph('', x0=x0, y0=y0, X=X, n=1)
        self.__exact = AnalGraph('', x0=x0, y0=y0, X=X, n=1)
        self.__x0 = x0
        self.__y0 = y0
        self.__X = X
        self.__name = name
        self.__xgrid = list(range(1, 100))
        self.__ygrid = []
    
    def recalculate(self, x0, y0, X):
        self.__x0 = x0
        self.__y0 = y0
        self.__X = X
        self.__ygrid.clear()
        for i in self.__xgrid:
            self.__approx.recalculate(self.__x0, self.__y0, self.__X, i)
            _, temp_approx, _ = self.__approx.get_grid()
            self.__exact.recalculate(self.__x0, self.__y0, self.__X, i)
            _, temp_exact, _ = self.__exact.get_grid()
            maxx = -1e10
            for e, a in zip(temp_exact, temp_approx):
                if e - a > maxx:
                    maxx = e - a
            self.__ygrid.append(maxx)
    
    def get_grid(self):
        return self.__xgrid, self.__ygrid, self.__name
